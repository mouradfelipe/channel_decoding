#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "pcg_variants.h"
/*#include "pcg_random.hpp"*/
#include <math.h>
#include <time.h>

/*#define M3*/
/*#define DEBUG*/
/*#define M4*/
/*#define M6*/

/*#define numIter 20*/

#ifdef M3
#define numberOfStates 8
#define filename "convm3varicao1.csv"
#elif defined(M4)
#define filename "convm4varicao1.csv"
#define numberOfStates 16
#elif defined(M6)
#define filename "convm6varicao1.csv"
#define numberOfStates 64
#endif

void bin(unsigned n) 
{ 
    unsigned i; 
    for (i = 1 << 7; i > 0; i = i / 2) 
        (n & i)? printf("1"): printf("0"); 
} 
void bin32(unsigned n) 
{ 
    unsigned i; 
    for (i = 1 << 31; i > 0; i = i / 2) 
        (n & i)? printf("1"): printf("0"); 
} 
void bin16(unsigned n) 
{ 
    unsigned i; 
    for (i = 1 << 15; i > 0; i = i / 2) 
        (n & i)? printf("1"): printf("0"); 
} 
// m = 3; 
// g1 = 13 = 001011 = 1 + 0D + D^2 + D^3; 
// g2 = 15 = 001101 = 1 + D + D^3; 
// g3 = 17 = 001111 = 1 + D + D^2 + D^3;
// m = 4;
// g1 = 25 = 010101 = 1 + 0D + 1D^2 + 0D^3 + 1^D4
// g2 = 33 = 011011 = 1 + 1D + 0D^2 + 1D^3 + 1^D4
// g3 = 37 = 011111 = 1 + 1D + 1D^2 + 1D^3 + 1^D4
// m = 6
// g1 = 117= 001001111 = 1 + 0D + 0D^2 + 1D^3 + 1D^4 + 1D^5 + 1D^6
// g3 = 127= 001010111 = 1 + 0D + 1D^2 + 0D^3 + 1D^4 + 1D^5 + 1D^6
// g1 = 155= 001101101 = 1 + 1D + 0D^2 + 1D^3 + 1D^4 + 0D^5 + 1D^6

/* Precisamos guardar para as duas entradas possíveis 0/1
 * o proximo estado 2*(m bits), e a saida correspondente 2*(3 bits)
 * ou seja, precisamos de 2m + 6 bits:
 * m = 3 -> 12 bits
 * m = 4 -> 14 bits
 * m = 6 -> 18 bits
 * Alem disso temos 2^m estados, portanto precisaremos de 2^m*(2m + 6) bits para
 * representar a matriz de transicao de estados
 * Outro detalhe é que nao eh possivel usar apenas o numero exato de bits calculados, pois o 
 * processador nao trabalha com bits isoladamente
 */

/* Utilizaremos structs contendo vetores de inteiros, onde cada elemento representa um linha na matriz
 * de transicao de estados correspondente ao i-esimo estado
 * m3
 * --  s1 s2 s3  o1 o2 o3 
 * 00  0  0  0   0  0  0
 * m4
 * --  s1 s2 s3 s4  o1 o2 o3 
 * 0   0  0  0  0    0  0  0
 * m6
 * -------    s1 s2 s3 s4 s5 s6 o1 o2 o3 
 * 00000000   0  0  0  0  0  0  0  0  0
 */

typedef struct MTable {
#ifdef M3
    uint8_t inputStates[2][numberOfStates];
#elif defined(M4)
    uint8_t inputStates[2][numberOfStates];
#elif defined(M6)
    uint16_t inputStates[2][numberOfStates];
#endif
    uint8_t currentState;
} MTable;

// Structs para facilitar a transmissao de mensagens
/* Guarda a messagem codificada, esta mensagem contem 30000 bits de informação, teoricamente precisariamos
 * de um array de 1250 por 24 bits, porem cada bloco possui o tamanho mais proximo que é um inteiro de
 * 32 bits, neste casso 8 bits em cada elemento do array nao estao sendo utilizados
 */
typedef struct CodedMessagePack {
    uint32_t message[1250];
} CodedMessagePack;

/* Guarda tanto a mensagem original quanto a mensagem decodificada, a mensagem contem 10000 bits,
 * organizados em um array de 1250 inteiros de 8bits
 */
typedef struct MessagePack {
    uint8_t message[1250];
} MessagePack;

/* Essa struct tem como objetivo rastrear valores importantes na decodificao de viterbi;
 * symbols[numberOfStates][mes] -> guarda o caminho sobrevivente até o estado k
 * onde k = numberOfStates*i + mes;
 * costStateK e costStateKplus1 guardam o custo do estado atual e do proximo estado;
 * hammingDistanceTable é utilizada para cache das possiveis distancias de hamming;
 */
typedef struct ViterbiData {
#ifdef M3
    uint8_t symbols[numberOfStates][1250];
    uint32_t costStateK[numberOfStates];
    uint32_t costStateKplus1[numberOfStates];
#elif defined(M4)
    uint8_t symbols[numberOfStates][1250];
    uint32_t costStateK[numberOfStates];
    uint32_t costStateKplus1[numberOfStates];
#elif defined(M6)
    uint8_t symbols[numberOfStates][1250];
    uint32_t costStateK[numberOfStates];
    uint32_t costStateKplus1[numberOfStates];
#endif
    uint8_t hammingDistanceTable[256];
} ViterbiData;

static inline uint8_t getTableOutput(MTable *table, const uint8_t binaryInput, const uint8_t currentState) {
    uint8_t output = table->inputStates[binaryInput][currentState] & 0x07;
    return output;
}

static inline uint8_t getNextState(MTable *table, const uint8_t binaryInput, const uint8_t currentState) {
    uint8_t nextState = (table->inputStates[binaryInput][currentState] >> 3) & 0x07;
    return nextState;
}

MTable createMTransitionTable(const uint8_t g1, const uint8_t g2, const uint8_t g3) {
    MTable table;
    // Para montar a matriz basta lembrarmos que na entrada acontece um shift a direita nas memorias 
    // enquanto a entrada vai para a primeira memoria
    for (uint32_t i = 0; i < numberOfStates; i++) {
        // Primeiramente calculamos a saida com o estado atual dos registradores 
        uint8_t S = i;
        uint8_t O = 0;
        /* Para calculo das saidas utilizamos uma operaçao AND entre o estado e a função g, note que para 
         * cada D^N precisamoresmo deslocar o bit o número de casas correspondente aos estados e após isso 
         * realizar uma mascara com 0x01
         */
        uint8_t sDotg1 = S & g1;
        uint8_t sDotg2 = S & g2;
        uint8_t sDotg3 = S & g3;
#ifdef M3
        // Acrescentamos a entrada 0 nas saidas 
        uint8_t o1 = 0x00 ^ ((sDotg1 >> 2) & 0x01) ^ ((sDotg1 >> 1) & 0x01) ^ ((sDotg1 >> 0) & 0x01);
        uint8_t o2 = 0x00 ^ ((sDotg2 >> 2) & 0x01) ^ ((sDotg2 >> 1) & 0x01) ^ ((sDotg2 >> 0) & 0x01);
        uint8_t o3 = 0x00 ^ ((sDotg3 >> 2) & 0x01) ^ ((sDotg3 >> 1) & 0x01) ^ ((sDotg3 >> 0) & 0x01);
        /* Após calculo da saida realizamos uma operacao OR para montar a saida total, conforme especificado
         * no comentario de MTable
         */
        O = (o1 << 2) | (o2 << 1) | o3;
        /* Realizamos um shift em S, que corresponde a um shift a direita nos registradores e inserimos
         * a entrada atual no primeiro registrador */
        S >>= 1;
        S &= 0x03;
        S = (S << 3) & 0x38;
        table.inputStates[0][i] = S | O;

        /* Realizamos o mesmo procedimento descrito acima para a entrada 1 abaixo */
        S = i;
        O = 0;
        // Acrescentamos a entrada 1 nas saidas calculadas acima
        o1 = 0x01 ^ o1;
        o2 = 0x01 ^ o2;
        o3 = 0x01 ^ o3;
        O = (o1 << 2) | (o2 << 1) | o3;
        S >>= 1;
        S |= 0x04;
        // 0x38 = 00111000
        S = (S << 3) & 0x38;
        table.inputStates[1][i] = S | O;
#elif defined(M4)
        // Acrescentamos a entrada 0 nas saidas 
        uint8_t o1 = 0x00 ^ ((sDotg1 >> 3) & 0x01) ^ 
                     ((sDotg1 >> 2) & 0x01) ^ ((sDotg1 >> 1) & 0x01) ^ ((sDotg1 >> 0) & 0x01);
        uint8_t o2 = 0x00 ^ ((sDotg2 >> 3) & 0x01) ^ 
                     ((sDotg2 >> 2) & 0x01) ^ ((sDotg2 >> 1) & 0x01) ^ ((sDotg2 >> 0) & 0x01);
        uint8_t o3 = 0x00 ^ ((sDotg3 >> 3) & 0x01) ^ 
                     ((sDotg3 >> 2) & 0x01) ^ ((sDotg3 >> 1) & 0x01) ^ ((sDotg3 >> 0) & 0x01);
        /* Após calculo da saida realizamos uma operacao OR para montar a saida total, conforme especificado
         * no comentario de MTable
         */
        O = (o1 << 2) | (o2 << 1) | o3;
        /* Realizamos um shift em S, que corresponde a um shift a direita nos registradores e inserimos
         * a entrada atual no primeiro registrador */
        S >>= 1;
        // 0x07 = 00000111
        S &= 0x07;
        // 0x78  = 01111000
        S = (S << 3) & 0x78;
        table.inputStates[0][i] = S | O;

        /* Realizamos o mesmo procedimento descrito acima para a entrada 1 abaixo */
        S = i;
        O = 0;
        // Acrescentamos a entrada 1 nas saidas calculadas acima
        o1 = 0x01 ^ o1;
        o2 = 0x01 ^ o2;
        o3 = 0x01 ^ o3;
        O = (o1 << 2) | (o2 << 1) | o3;
        S >>= 1;
        // 0x08 = 00001000
        S |= 0x08;
        S = (S << 3) & 0x78;
        table.inputStates[1][i] = S | O;
#elif defined(M6)
        // Acrescentamos a entrada 0 nas saidas 
        uint8_t o1 = 0x00 ^ ((sDotg1 >> 5) & 0x01) ^ ((sDotg1 >> 4) & 0x01) ^ 
                     ((sDotg1 >> 3) & 0x01) ^ ((sDotg1 >> 2) & 0x01) ^ 
                     ((sDotg1 >> 1) & 0x01) ^ ((sDotg1 >> 0) & 0x01);
        uint8_t o2 = 0x00 ^ ((sDotg2 >> 5) & 0x01) ^ ((sDotg2 >> 4) & 0x01) ^ 
                     ((sDotg2 >> 3) & 0x01) ^ ((sDotg2 >> 2) & 0x01) ^ 
                     ((sDotg2 >> 1) & 0x01) ^ ((sDotg2 >> 0) & 0x01);
        uint8_t o3 = 0x00 ^ ((sDotg3 >> 5) & 0x01) ^ ((sDotg3 >> 4) & 0x01) ^ 
                     ((sDotg3 >> 3) & 0x01) ^ ((sDotg3 >> 2) & 0x01) ^ 
                     ((sDotg3 >> 1) & 0x01) ^ ((sDotg3 >> 0) & 0x01);
        /* Após calculo da saida realizamos uma operacao OR para montar a saida total, conforme especificado
         * no comentario de MTable
         */
        O = (o1 << 2) | (o2 << 1) | o3;
        /* Realizamos um shift em S, que corresponde a um shift a direita nos registradores e inserimos
         * a entrada atual no primeiro registrador */
        S >>= 1;
        // 0x1f = 00011111
        S &= 0x1f;
        // 0x01f8  = 0000 0001 1111 1000
        uint16_t state  = S;
        state = (state << 3) & 0x01f8;
        table.inputStates[0][i] = state | O;

        /* Realizamos o mesmo procedimento descrito acima para a entrada 1 abaixo */
        S = i;
        O = 0;
        // Acrescentamos a entrada 1 nas saidas calculadas acima
        o1 = 0x01 ^ o1;
        o2 = 0x01 ^ o2;
        o3 = 0x01 ^ o3;
        O = (o1 << 2) | (o2 << 1) | o3;
        S >>= 1;
        // 0x20 = 00100000
        S |= 0x20;
        state = S;
        state = (state << 3) & 0x01f8;
        table.inputStates[1][i] = state | O;
#endif
    }
    return table;
}

/* O codificado simula a execucao da maquina de estados de acordo com a tabela de transicao de estados
 */
CodedMessagePack encoder(MTable *table, MessagePack* message) {
    CodedMessagePack codePack;
#ifdef M3
    uint8_t stateMask = 0x07;
#elif defined(M4)
    uint8_t stateMask = 0x0f;
#elif defined(M6)
    uint8_t stateMask = 0x3f;
#endif
    for (uint32_t m = 0; m < 1250; m++) {
        uint8_t info = message->message[m];
        uint32_t code = 0;
        for (int8_t i = 7; i >= 0; i--) {
            uint8_t bit = (info >> i) & 0x01;
            // recupera o bit codificado 
            uint8_t partialCode = table->inputStates[bit][table->currentState] & 0x07;
            // atualiza o estados atual da maquina de estados
            table->currentState = (table->inputStates[bit][table->currentState] >> 3) & stateMask;
            // desloca os 3 bits do codigo para a posicao correta no bloco decodificado
            code |= (partialCode << i*3);
        }
        codePack.message[m] = code;


    }
    return codePack;
}

MessagePack decoder(MTable *table, CodedMessagePack* codedMessage) {
#ifdef M3
    uint8_t stateMask = 0x07;
#elif defined(M4)
    uint8_t stateMask = 0x0f;
#elif defined(M6)
    uint8_t stateMask = 0x3f;
#endif
    ViterbiData data = { {{0}, {0}}, {UINT32_MAX/2}, {UINT32_MAX/2}, {0} };
    MessagePack message;

    for (uint32_t s = 0 ; s < numberOfStates; s++) {
        data.costStateK[s] = UINT32_MAX/2;
        data.costStateKplus1[s] = UINT32_MAX/2;
    }
    for (uint32_t i = 0; i < 8; i++) {
        uint8_t distance = 0;
        uint8_t x = i;
        while (x > 0) {
            distance += x & 0x01;
            x >>= 1;
        }
        data.hammingDistanceTable[i] = distance;
    }
    data.costStateK[0] = 0;
    uint8_t totalPath[numberOfStates][1250];
    uint8_t codes[8];
    for (uint32_t m = 0; m < 1250; m++) {
        uint8_t actualPath[numberOfStates] = {0};
        for (int8_t k = 0; k < 8; k++) {
            codes[k] = (codedMessage->message[m] >> k*3) & 0x07;
        }
        for (int8_t k = 7; k >= 0; k--) {
#ifdef DEBUG
            printf(" current m: %d, current k: %d\n", m, k);
#endif
            uint8_t code = codes[k];
            for (uint32_t i = 0; i < numberOfStates; i++) {
                if (data.costStateK[i] < UINT32_MAX/2) {
                    // Entrada 0
#ifdef DEBUG
                    printf("\npath: ");
                    bin(actualPath[i]);
                    printf("\n");
                    printf("i: %d", i);
                    printf("\n");
#endif
                    uint8_t j0 = (table->inputStates[0][i] >> 3) & stateMask;
                    uint8_t out0 = table->inputStates[0][i] & 0x07;
                    uint8_t distance0 = data.hammingDistanceTable[code ^ out0];
                    uint32_t cost0 = data.costStateK[i] + distance0;
                    if ( cost0 < data.costStateKplus1[j0] ) {
#ifdef DEBUG
                        printf("j0: %d\n", j0);
                        printf("code: ");
                        bin(code);
                        printf("\n");
                        printf("b0: ");
                        bin(out0);
                        printf("\n");
                        printf("distance0: %d \n", distance0);
#endif
                        data.costStateKplus1[j0] = cost0;
                        data.symbols[j0][m] = actualPath[i] & (~(1 << k));
                        data.symbols[j0][m] = actualPath[i] | (0 << k);
                        if (m > 0)
                            memcpy(data.symbols[j0], totalPath[i], m);
#ifdef DEBUG
                        uint8_t mes = data.symbols[j0][m];
                        printf("mes: ");
                        bin(mes);
                        printf("\n");
#endif
                    }
                    // Entrada 1
                    uint8_t j1 = (table->inputStates[1][i] >> 3) & stateMask;
                    uint8_t out1 = table->inputStates[1][i] & 0x07;
                    uint8_t distance1 = data.hammingDistanceTable[code ^ out1];
                    uint32_t cost1 = data.costStateK[i] + distance1;
                    if ( cost1 < data.costStateKplus1[j1] ) {
#ifdef DEBUG
                        printf("j1: %d\n", j1);
                        printf("code: ");
                        bin(code);
                        printf("\n");
                        printf("b1: ");
                        bin(out1);
                        printf("\n");
                        printf("distance1: %d \n", distance1);
#endif
                        data.costStateKplus1[j1] = cost1;
                        data.symbols[j1][m] = actualPath[i] & (~(1 << k));
                        data.symbols[j1][m] = actualPath[i] | (1 << k);
                        if (m > 0)
                            memcpy(data.symbols[j1], totalPath[i], m);
#ifdef DEBUG
                        uint8_t mes = data.symbols[j1][m];
                        printf("mes: ");
                        bin(mes);
                        printf("\n");
#endif
                    }
                }
            }
            for (uint32_t s = 0 ; s < numberOfStates; s++) {
                if (m > 0)
                    memcpy(totalPath[s], data.symbols[s], m);
                actualPath[s] = data.symbols[s][m];
                data.costStateK[s] = data.costStateKplus1[s];
#ifdef DEBUG
                printf("cost : %d\n", data.costStateK[s]);
#endif
                data.costStateKplus1[s] = UINT32_MAX/2;
            }
        }
        for (uint8_t s = 0 ; s < numberOfStates; s++) {
            memcpy(totalPath[s], data.symbols[s], m+1);
        }
    }
    uint32_t minCost = UINT32_MAX;
    uint32_t minJ = 0;
    for (uint32_t j = 0; j < numberOfStates; j++) {
        if (data.costStateK[j] < minCost) {
            minCost = data.costStateK[j];
            minJ = j;
        }
    }
    /*printf("\n \n code: ");*/
    /*bin(data.symbols[minJ][0]);*/
    /*printf("\n");*/
    memcpy(&message.message, data.symbols[minJ], sizeof(message.message));
    return message;
}

pcg8i_random_t rng8;
MessagePack createMessage() {
    MessagePack message;
    pcg8i_srandom_r(&rng8, time(NULL), (intptr_t)&rng8);
    message.message[0] = 0b11101011;
    message.message[1] = 0b11101011;
    message.message[2] = 0b11101011;
    for (uint32_t i = 0; i < 1250; i++) {
        /*message.message[i] = i % 256;*/
        message.message[i] = pcg8i_random_r(&rng8); 
    }
    return message;
}

CodedMessagePack bscChannel(CodedMessagePack *message, double p) {
    CodedMessagePack errorMessage;
    pcg64_random_t rng;
    pcg64_srandom_r(&rng, time(NULL), (intptr_t)&rng);
    for (uint32_t m = 0; m < 1250; m++) {
        uint32_t mask = 0;
        for (int8_t k = 23; k >= 0; k--) {
            double d = ldexp(pcg64_random_r(&rng), -64);
            if (d < p) {
                mask |= (1 << k);
            }
        }
        errorMessage.message[m] = message->message[m] ^ mask;
    }
    return errorMessage;
}

MessagePack bscChannelMsg(MessagePack *message, double p) {
    MessagePack errorMessage;
    pcg64_random_t rng;
    pcg64_srandom_r(&rng, time(NULL), (intptr_t)&rng);
    for (uint32_t m = 0; m < 1250; m++) {
        uint32_t mask = 0;
        for (int8_t k = 7; k >= 0; k--) {
            double d = ldexp(pcg64_random_r(&rng), -64);
            if (d < p) {
                mask |= (1 << k);
            }
        }
        errorMessage.message[m] = message->message[m] ^ mask;
    }
    return errorMessage;
}


uint64_t error(MessagePack *orgMsg, MessagePack *decodedMsg) {
    uint8_t hammingDistanceTable[256];
    for (uint32_t i = 0; i < 256; i++) {
        uint8_t distance = 0;
        uint8_t x = i;
        while (x > 0) {
            distance += x & 0x01;
            x >>= 1;
        }
        hammingDistanceTable[i] = distance;
    }
    uint64_t distance = 0;
    for (uint32_t m = 0; m < 1250; m++) {
        uint8_t decMsg = decodedMsg->message[m];
        uint8_t msg = orgMsg->message[m];
        distance += hammingDistanceTable[decMsg^msg];
    }
    return distance;
}




int main() {
    MTable mTable;
#ifdef M3
    uint8_t g1 = 013;
    uint8_t g2 = 015;
    uint8_t g3 = 017;
#elif defined(M4)
    uint8_t g1 = 025;
    uint8_t g2 = 033;
    uint8_t g3 = 037;
#elif defined(M6)
    uint8_t g1 = 0117;
    uint8_t g2 = 0127;
    uint8_t g3 = 0155;
#endif
    /*double probs[3] = {0.5, 0.2, 0.1};*/
    double probs[20] = {0.327360423009289, 0.198764260392861, 0.133550095018059, 0.0931039503948837, 0.0662418306202036, 0.0477554618894513, 0.0347511220824595, 0.0254657221008204, 0.0187636948208680, 0.0138864847984315, 0.0103143310054568, 0.00768442752908296, 0.00573995307624579, 0.00429711878505383, 0.00322325455915736, 0.00242191456899947, 0.00182257811075301, 0.00137342938550014, 0.00103623888325758, 0.000782701129001274};
    mTable = createMTransitionTable(g1, g2, g3);
    double errorBsc[numIter][40];
    double errorWbsc[numIter][40];
    int k = 0;
    FILE *fp;
    fp=fopen(filename,"w+");
    /*int numIter = 100;*/
    clock_t start, end;
    double cpu_time_used;
    double encodedTime = 0;
    double decodedTime = 0;
    int count = 0;
    for(int m = 0; m < numIter; m++) {
        k = 0;
        printf("m: %d\n", m);
        for(int i = 0; i < 20; i += 1) {
            /*for(int j = 0; j < 3; j++) {*/
                /*double p = probs[j]/i;*/
                double p = probs[i];
                mTable.currentState = 0;
                MessagePack message = createMessage();
                MessagePack errorMessage = bscChannelMsg(&message, p);
                start = clock();
                CodedMessagePack codePack = encoder(&mTable, &message);
                end = clock();
                encodedTime += ((double) (end - start)) / CLOCKS_PER_SEC;
                uint32_t code = codePack.message[0];
                CodedMessagePack bscCodeMessage = bscChannel(&codePack, p);
                /*printf("code: ");*/
                /*bin32(code);*/
                /*printf("\n \n");*/
                start = clock();
                MessagePack decoded = decoder(&mTable, &bscCodeMessage);
                end = clock();
                decodedTime += ((double) (end - start)) / CLOCKS_PER_SEC;
                /*for (uint32_t i = 0; i < 1250; i++) {*/
                    /*uint8_t info = message.message[i];*/
                    /*uint8_t cod = decoded.message[i];*/
                    /*[>printf("i: %d \n", i);<]*/
                    /*if((info^cod) > 0) {*/
                        /*printf("mess: ");*/
                        /*bin(info);*/
                        /*printf("\n");*/
                        /*printf("code: ");*/
                        /*bin(cod);*/
                        /*printf("\n\n");*/
                    /*}*/
                /*}*/
                
                /*printf("O erro para p: %.10f foi de: %f\% \n", p, (double)error(&message, &decoded)/100);*/
                /*printf("O erro para p: %.10f sem codificacao foi de: %f\% \n", p, (double)error(&message, &errorMessage)/100);*/
                /*printf("\n");*/
                /*fprintf(fp, "\n%.10f,%.10f,%.10f ", p, (double)error(&message, &decoded)/100, (double)error(&message, &errorMessage)/100);*/
                errorBsc[m][k] = (double)error(&message, &decoded)/10000.0;
                errorWbsc[m][k] = (double)error(&message, &errorMessage)/10000.0;
                k++;
                count++;
            /*}*/
        }
    }
    k = 0;
    for(int i = 0; i < 20; i += 1) {
        /*for(int j = 0; j < 3; j++) {*/
            /*double p = probs[j]/i;*/
            double p = probs[i];
            double media1 = 0;
            double media2 = 0;
            double var = 0;
            for (int m = 0; m < numIter; m++) {
                media1 += errorBsc[m][k];
                media2 += errorWbsc[m][k];
            }
            media1 = media1/numIter;
            media2 = media2/numIter;
            for (int m = 0; m < numIter; m++) {
                var += (errorBsc[m][k] - media1)*(errorBsc[m][k] - media1);
            }
            fprintf(fp, "\n%.10f,%.30lf,%.30lf, %.30lf ", p, media1, media2, var);
                    
            k++;
        /*}*/
    }
    printf("O tempo medio para codificacao foi de: %.20lf e o de decodificacao foi de %.20lf microsegundos\n",
            (encodedTime/count/10000.0)*1000000.0, (decodedTime/count/10000.0)*1000000.0);
    fclose(fp);

}
