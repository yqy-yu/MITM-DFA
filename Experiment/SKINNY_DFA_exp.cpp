#include <iostream>
#include <map>
using namespace std;

// 8-bit Sbox
const uint8_t S[256] = {0x65, 0x4c, 0x6a, 0x42, 0x4b, 0x63, 0x43, 0x6b, 0x55, 0x75, 0x5a, 0x7a, 0x53, 0x73, 0x5b, 0x7b, 0x35, 0x8c, 0x3a, 0x81, 0x89, 0x33, 0x80, 0x3b, 0x95, 0x25, 0x98, 0x2a, 0x90, 0x23, 0x99, 0x2b, 0xe5, 0xcc, 0xe8, 0xc1, 0xc9, 0xe0, 0xc0, 0xe9, 0xd5, 0xf5, 0xd8, 0xf8, 0xd0, 0xf0, 0xd9, 0xf9, 0xa5, 0x1c, 0xa8, 0x12, 0x1b, 0xa0, 0x13, 0xa9, 0x05, 0xb5, 0x0a, 0xb8, 0x03, 0xb0, 0x0b, 0xb9, 0x32, 0x88, 0x3c, 0x85, 0x8d, 0x34, 0x84, 0x3d, 0x91, 0x22, 0x9c, 0x2c, 0x94, 0x24, 0x9d, 0x2d, 0x62, 0x4a, 0x6c, 0x45, 0x4d, 0x64, 0x44, 0x6d, 0x52, 0x72, 0x5c, 0x7c, 0x54, 0x74, 0x5d, 0x7d, 0xa1, 0x1a, 0xac, 0x15, 0x1d, 0xa4, 0x14, 0xad, 0x02, 0xb1, 0x0c, 0xbc, 0x04, 0xb4, 0x0d, 0xbd, 0xe1, 0xc8, 0xec, 0xc5, 0xcd, 0xe4, 0xc4, 0xed, 0xd1, 0xf1, 0xdc, 0xfc, 0xd4, 0xf4, 0xdd, 0xfd, 0x36, 0x8e, 0x38, 0x82, 0x8b, 0x30, 0x83, 0x39, 0x96, 0x26, 0x9a, 0x28, 0x93, 0x20, 0x9b, 0x29, 0x66, 0x4e, 0x68, 0x41, 0x49, 0x60, 0x40, 0x69, 0x56, 0x76, 0x58, 0x78, 0x50, 0x70, 0x59, 0x79, 0xa6, 0x1e, 0xaa, 0x11, 0x19, 0xa3, 0x10, 0xab, 0x06, 0xb6, 0x08, 0xba, 0x00, 0xb3, 0x09, 0xbb, 0xe6, 0xce, 0xea, 0xc2, 0xcb, 0xe3, 0xc3, 0xeb, 0xd6, 0xf6, 0xda, 0xfa, 0xd3, 0xf3, 0xdb, 0xfb, 0x31, 0x8a, 0x3e, 0x86, 0x8f, 0x37, 0x87, 0x3f, 0x92, 0x21, 0x9e, 0x2e, 0x97, 0x27, 0x9f, 0x2f, 0x61, 0x48, 0x6e, 0x46, 0x4f, 0x67, 0x47, 0x6f, 0x51, 0x71, 0x5e, 0x7e, 0x57, 0x77, 0x5f, 0x7f, 0xa2, 0x18, 0xae, 0x16, 0x1f, 0xa7, 0x17, 0xaf, 0x01, 0xb2, 0x0e, 0xbe, 0x07, 0xb7, 0x0f, 0xbf, 0xe2, 0xca, 0xee, 0xc6, 0xcf, 0xe7, 0xc7, 0xef, 0xd2, 0xf2, 0xde, 0xfe, 0xd7, 0xf7, 0xdf, 0xff};
// 8-bit Sbox Inverse
const uint8_t Sinv[256] = {0xac, 0xe8, 0x68, 0x3c, 0x6c, 0x38, 0xa8, 0xec, 0xaa, 0xae, 0x3a, 0x3e, 0x6a, 0x6e, 0xea, 0xee, 0xa6, 0xa3, 0x33, 0x36, 0x66, 0x63, 0xe3, 0xe6, 0xe1, 0xa4, 0x61, 0x34, 0x31, 0x64, 0xa1, 0xe4, 0x8d, 0xc9, 0x49, 0x1d, 0x4d, 0x19, 0x89, 0xcd, 0x8b, 0x8f, 0x1b, 0x1f, 0x4b, 0x4f, 0xcb, 0xcf, 0x85, 0xc0, 0x40, 0x15, 0x45, 0x10, 0x80, 0xc5, 0x82, 0x87, 0x12, 0x17, 0x42, 0x47, 0xc2, 0xc7, 0x96, 0x93, 0x03, 0x06, 0x56, 0x53, 0xd3, 0xd6, 0xd1, 0x94, 0x51, 0x04, 0x01, 0x54, 0x91, 0xd4, 0x9c, 0xd8, 0x58, 0x0c, 0x5c, 0x08, 0x98, 0xdc, 0x9a, 0x9e, 0x0a, 0x0e, 0x5a, 0x5e, 0xda, 0xde, 0x95, 0xd0, 0x50, 0x05, 0x55, 0x00, 0x90, 0xd5, 0x92, 0x97, 0x02, 0x07, 0x52, 0x57, 0xd2, 0xd7, 0x9d, 0xd9, 0x59, 0x0d, 0x5d, 0x09, 0x99, 0xdd, 0x9b, 0x9f, 0x0b, 0x0f, 0x5b, 0x5f, 0xdb, 0xdf, 0x16, 0x13, 0x83, 0x86, 0x46, 0x43, 0xc3, 0xc6, 0x41, 0x14, 0xc1, 0x84, 0x11, 0x44, 0x81, 0xc4, 0x1c, 0x48, 0xc8, 0x8c, 0x4c, 0x18, 0x88, 0xcc, 0x1a, 0x1e, 0x8a, 0x8e, 0x4a, 0x4e, 0xca, 0xce, 0x35, 0x60, 0xe0, 0xa5, 0x65, 0x30, 0xa0, 0xe5, 0x32, 0x37, 0xa2, 0xa7, 0x62, 0x67, 0xe2, 0xe7, 0x3d, 0x69, 0xe9, 0xad, 0x6d, 0x39, 0xa9, 0xed, 0x3b, 0x3f, 0xab, 0xaf, 0x6b, 0x6f, 0xeb, 0xef, 0x26, 0x23, 0xb3, 0xb6, 0x76, 0x73, 0xf3, 0xf6, 0x71, 0x24, 0xf1, 0xb4, 0x21, 0x74, 0xb1, 0xf4, 0x2c, 0x78, 0xf8, 0xbc, 0x7c, 0x28, 0xb8, 0xfc, 0x2a, 0x2e, 0xba, 0xbe, 0x7a, 0x7e, 0xfa, 0xfe, 0x25, 0x70, 0xf0, 0xb5, 0x75, 0x20, 0xb0, 0xf5, 0x22, 0x27, 0xb2, 0xb7, 0x72, 0x77, 0xf2, 0xf7, 0x2d, 0x79, 0xf9, 0xbd, 0x7d, 0x29, 0xb9, 0xfd, 0x2b, 0x2f, 0xbb, 0xbf, 0x7b, 0x7f, 0xfb, 0xff};
// Permutation
const uint8_t P[16] = {0x0, 0x1, 0x2, 0x3, 0x7, 0x4, 0x5, 0x6, 0xa, 0xb, 0x8, 0x9, 0xd, 0xe, 0xf, 0xc};
const uint8_t Pinv[16] = {0x0, 0x1, 0x2, 0x3, 0x5, 0x6, 0x7, 0x4, 0xa, 0xb, 0x8, 0x9, 0xf, 0xc, 0xd, 0xe};
// Tweakey Permutation
const uint8_t Q[16] = {0x9, 0xf, 0x8, 0xd, 0xa, 0xe, 0xc, 0xb, 0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7};
// Round Constants
const uint8_t RC[62] = {0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F,
                        0x1E, 0x3C, 0x39, 0x33, 0x27, 0x0E, 0x1D, 0x3A, 0x35, 0x2B,
                        0x16, 0x2C, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0B, 0x17, 0x2E,
                        0x1C, 0x38, 0x31, 0x23, 0x06, 0x0D, 0x1B, 0x36, 0x2D, 0x1A,
                        0x34, 0x29, 0x12, 0x24, 0x08, 0x11, 0x22, 0x04, 0x09, 0x13,
                        0x26, 0x0c, 0x19, 0x32, 0x25, 0x0a, 0x15, 0x2a, 0x14, 0x28,
                        0x10, 0x20};
multimap<uint64_t,uint32_t> Delta_key_x_1;
multimap<uint64_t,uint32_t> Delta_key_x_13;

multimap<uint64_t,uint32_t> Delta_key_x_3;
multimap<uint64_t,uint32_t> Delta_key_x_15;

multimap<uint64_t,uint32_t> Delta_key_x_6;
multimap<uint64_t,uint32_t> Delta_key_x_14;

void mix_columns(uint8_t state[16]);
void inv_mix_columns(uint8_t state[16]);
void tweakey_schedule(int rounds, uint8_t tk[][16], uint8_t round_tweakey[][8]);
void enc(int R, uint8_t plaintext[16], uint8_t ciphertext[16], uint8_t tk[][8]);
void enc_e_32_13(int R, uint8_t plaintext[16], uint8_t ciphertext[16], uint8_t tk[][8], uint8_t e);

uint8_t Compute_13(uint8_t ciphertext[16], uint8_t tweakey1[3]);
uint8_t Compute_1(uint8_t ciphertext[16], uint8_t tweakey1[3]);
void Creat_Table_13(uint8_t c[][16], uint8_t cx[][16]);
void Creat_Table_1(uint8_t c[][16], uint8_t cx[][16]);

void enc_e_32_15(int R, uint8_t plaintext[16], uint8_t ciphertext[16], uint8_t tk[][8], uint8_t e);
uint8_t Compute_15(uint8_t ciphertext[16], uint8_t tweakey1[3], uint8_t tk_9);
uint8_t Compute_3(uint8_t ciphertext[16], uint8_t tweakey1[3], uint8_t tk_15);
void Creat_Table_3(uint8_t c[][16], uint8_t cx[][16], uint8_t tk_15);
void Creat_Table_15(uint8_t c[][16], uint8_t cx[][16], uint8_t tk_9);

uint8_t Compute_14(uint8_t ciphertext[16], uint8_t tweakey1[3], uint8_t tk_13);
uint8_t Compute_6(uint8_t ciphertext[16], uint8_t tweakey1[3], uint8_t tk_15, uint8_t tk_6);
void Creat_Table_6(uint8_t c[][16], uint8_t cx[][16], uint8_t tk_15, uint8_t tk_6);
void Creat_Table_14(uint8_t c[][16], uint8_t cx[][16], uint8_t tk_13);

void Creat_Table_14(uint8_t c[][16], uint8_t cx[][16], uint8_t tk_13){                          // Creat the matching table of delta X_14
    Delta_key_x_14.clear();
    for(int i=0;i<=255;i++){  
        for(int j=0;j<=255;j++){
            uint8_t key_guess[2]={i,j};
            uint8_t x1[12];
            for(int l=0;l<8;l++){
                if(l%2==0)    x1[l]=Compute_14(c[l/2], key_guess, tk_13);
                else x1[l]=Compute_14(cx[l/2], key_guess, tk_13);
            }
            uint8_t delta[6];                                                                   // Compute the delta
            for(int l=0;l<4;l++){
                delta[l]=x1[2*l]^x1[2*l+1];
            }
            uint64_t d=0;                                                                       // storage all delta in d
            for(int n=0;n<4;n++){
                d=(d << 8) | delta[n];
            }
            uint32_t ktp=0;                                                                     // storage all key in ktp
            ktp=i;
            ktp=(ktp<<8)|j;
            Delta_key_x_14.insert(make_pair(d,ktp));                        
        }
    }
}

void Creat_Table_6(uint8_t c[][16], uint8_t cx[][16], uint8_t tk_15, uint8_t tk_6){             // Creat the matching table of delta X_6
    Delta_key_x_6.clear();
    for(int i=0;i<=255;i++){                                                                     
        for(int j=0;j<=255;j++){
            uint8_t key_guess[2]={i,j};
            uint8_t x1[12];
            for(int l=0;l<8;l++){
                if(l%2==0)    x1[l]=Compute_6(c[l/2], key_guess, tk_15, tk_6);
                else x1[l]=Compute_6(cx[l/2], key_guess, tk_15, tk_6);
            }
            uint8_t delta[6];
            for(int l=0;l<4;l++){
                delta[l]=x1[2*l]^x1[2*l+1];
            }    
            uint64_t d=0;
            for(int n=0;n<4;n++){
                d=(d << 8) | delta[n];

            }
            uint32_t ktp=0;
            ktp=i;
            ktp=(ktp<<8)|j;
            Delta_key_x_6.insert(make_pair(d,ktp));

        }
    }
}

uint8_t Compute_14(uint8_t ciphertext[16], uint8_t tweakey1[2], uint8_t tk_13){                 //Compute the 14th cell from the ciphertext
    uint8_t tp[10];
    tp[0]=ciphertext[6]^ciphertext[10]^ciphertext[14];
    tp[0]^=tweakey1[1];
    tp[0]=Sinv[tp[0]];
    tp[0]^=tweakey1[0];
    tp[0]=Sinv[tp[0]];

    tp[1]=ciphertext[4];
    tp[1]^=(RC[39] & 0xf);
    tp[1]^=tk_13;
    tp[1]=Sinv[tp[1]];

    tp[2]=ciphertext[3]^ciphertext[15];
    tp[2]=Sinv[tp[2]];
    tp[2]^=tp[1];
    tp[2]=Sinv[tp[2]];
    tp[2]^=tp[0];
    tp[2]=Sinv[tp[2]];
    return tp[2];
}

uint8_t Compute_6( uint8_t ciphertext[16], uint8_t tweakey1[2] , uint8_t tk_15, uint8_t tk_6){                  //Compute the 6th cell from the ciphertext
    uint8_t tp[10];
    tp[0]=ciphertext[5]^ciphertext[9]^ciphertext[13];
    tp[0]^=tk_15;
    tp[0]^=((RC[39] >> 4) & 0x3);
    tp[0]=Sinv[tp[0]];

    tp[1]=ciphertext[6]^ciphertext[14];
    tp[1]^=0x2;
    tp[1]=Sinv[tp[1]];

    tp[2]=ciphertext[3]^ciphertext[15];
    tp[2]=Sinv[tp[2]];

    tp[3]= tp[0]^tp[1]^tp[2];
    tp[3]^=tk_6;
    tp[3]=Sinv[tp[3]];

    tp[4]=ciphertext[6]^ciphertext[10]^ciphertext[14];
    tp[4]^=tweakey1[0];
    tp[4]=Sinv[tp[4]];
    tp[5]=ciphertext[0]^ciphertext[12];
    tp[5]=Sinv[tp[5]];
    tp[5]^=tp[4];
    tp[5]=Sinv[tp[5]];

    tp[6]=ciphertext[6];
    tp[6]^=tweakey1[1];
    tp[6]=Sinv[tp[6]];
    tp[7]=ciphertext[1]^ciphertext[13];
    tp[7]=Sinv[tp[7]];
    tp[7]^=tp[6];
    tp[7]=Sinv[tp[7]];
    tp[7]^=tp[3]^tp[5];
    tp[7]^=tweakey1[0];
    tp[7]=Sinv[tp[7]];
    return tp[7];
}

void Creat_Table_15(uint8_t c[][16], uint8_t cx[][16], uint8_t tk_9){                                           // Creat the matching table of delta X_15
    Delta_key_x_15.clear();
    for(int i=0;i<=255;i++){
        for(int j=0;j<=255;j++){
            uint8_t key_guess[2]={i,j};
            uint8_t x1[12];
            for(int l=0;l<8;l++){
                if(l%2==0)    x1[l]=Compute_15(c[l/2], key_guess, tk_9);
                else x1[l]=Compute_15(cx[l/2], key_guess, tk_9);
            }
            uint8_t delta[6];
            for(int l=0;l<4;l++){
                delta[l]=x1[2*l]^x1[2*l+1];
            }
            uint64_t d=0;
            for(int n=0;n<4;n++){
                d=(d << 8) | delta[n];
            }
            uint32_t ktp=0;
            ktp=i;
            ktp=(ktp<<8)|j;
            Delta_key_x_15.insert(make_pair(d,ktp));
        }
    }
}

void Creat_Table_3(uint8_t c[][16], uint8_t cx[][16], uint8_t tk_15){                                       // Creat the matching table of delta X_3
    Delta_key_x_3.clear();
    for(int i=0;i<=255;i++){
        //cout<<(int)i;
        for(int j=0;j<=255;j++){
            uint8_t key_guess[2]={i,j};
            uint8_t x1[12];
            for(int l=0;l<8;l++){
                if(l%2==0)    x1[l]=Compute_3(c[l/2], key_guess, tk_15);
                else x1[l]=Compute_3(cx[l/2], key_guess, tk_15);
            }
            uint8_t delta[6];
            for(int l=0;l<4;l++){
                delta[l]=x1[2*l]^x1[2*l+1];
            }          
            uint64_t d=0;
            for(int n=0;n<4;n++){
                d=(d << 8) | delta[n];;
            }
            uint32_t ktp=0;
            ktp=i;
            ktp=(ktp<<8)|j;
            Delta_key_x_3.insert(make_pair(d,ktp));
        }
    }
}

uint8_t Compute_15(uint8_t ciphertext[16], uint8_t tweakey1[2], uint8_t tk_9){                          //Compute the 15th cell from the ciphertext
    uint8_t tp[10];
    tp[0]=ciphertext[7]^ciphertext[11]^ciphertext[15];
    tp[1]=ciphertext[5];
    tp[2]=ciphertext[12]^ciphertext[0];

    tp[0]^=tk_9;
    tp[1]^=tweakey1[1];
    for(int i=0;i<3;i++){
        tp[i]=Sinv[tp[i]];
    }
    tp[2]=tp[1]^tp[2];
    tp[0]^=tweakey1[0];
    tp[2]=Sinv[tp[2]];
    tp[0]=Sinv[tp[0]];
    tp[2]^=tp[0];
    tp[2]=Sinv[tp[2]];
    return tp[2];
}


uint8_t Compute_3( uint8_t ciphertext[16], uint8_t tweakey1[2] , uint8_t tk_15){                          //Compute the 3th cell from the ciphertext
    uint8_t tp[10];
    tp[0]=ciphertext[5]^ciphertext[9]^ciphertext[13];
    tp[0]^=tk_15;
    tp[0]^=((RC[39] >> 4) & 0x3);
    tp[0]=Sinv[tp[0]];

    tp[1]=ciphertext[6]^ciphertext[14];
    tp[1]^=0x2;
    tp[1]=Sinv[tp[1]];

    tp[2]=ciphertext[3]^ciphertext[15];
    tp[2]=Sinv[tp[2]];

    tp[3]= tp[0]^tp[1]^tp[2];
    tp[3]^=tweakey1[0];
    tp[3]=Sinv[tp[3]];
    tp[3]^=tweakey1[1];
    tp[3]=Sinv[tp[3]];
    return tp[3];
}

void enc_e_32_15(int R, uint8_t plaintext[16], uint8_t ciphertext[16], uint8_t tk[][8], uint8_t e)            //encrypt with difference in 15th cell of the 32nd round
{
    for (uint8_t i = 0; i < 16; i++)
    {
        ciphertext[i] = plaintext[i] & 0xff;
    }
    for (uint8_t r = 0; r < R; r++)
    {
        if(r==31){
            ciphertext[15]^=e;
        }
        // SBox
        for (uint8_t i = 0; i < 16; i++)
            ciphertext[i] = S[ciphertext[i]];
        // Add constants (constants only affects on three upper cells of the first column)
        ciphertext[0] ^= (RC[r] & 0xf);
        ciphertext[4] ^= ((RC[r] >> 4) & 0x3);
        ciphertext[8] ^= 0x2;
        // Add round tweakey (tweakey only exclusive-ored with two upper rows of the state)
        for (uint8_t i = 0; i < 8; i++)
            ciphertext[i] ^= tk[r][i];
        // Permute nibbles
        uint8_t temp[16];
        for (uint8_t i = 0; i < 16; i++)
            temp[i] = ciphertext[i];
        for (uint8_t i = 0; i < 16; i++)
            ciphertext[i] = temp[P[i]];
        // MixColumn
        mix_columns(ciphertext);
    }
}

void Creat_Table_13(uint8_t c[][16], uint8_t cx[][16]){                                                             // Creat the matching table of delta X_13
    for(int i=0;i<=255;i++){
        for(int j=0;j<=255;j++){
            for(int k=0;k<255;k++){
                uint8_t key_guess[3]={i,j,k};
                uint8_t x1[12];
                for(int l=0;l<12;l++){
                    if(l%2==0)  x1[l]=Compute_13(c[l/2],key_guess);
                    else x1[l]=Compute_13(cx[l/2],key_guess);
                }
                uint8_t delta[6];
                for(int l=0;l<6;l++){
                    delta[l]=x1[2*l]^x1[2*l+1];
                }                
                uint64_t d=0;                                              
                for(int n=0;n<6;n++){
                    d=(d << 8) | delta[n];
                }
                uint32_t ktp=0;                                             
                ktp=i;
                ktp=(ktp<<8)|j;
                ktp=(ktp<<8)|k;
                Delta_key_x_13.insert(make_pair(d,ktp));
            }
        }
    }
}

void Creat_Table_1(uint8_t c[][16], uint8_t cx[][16]){                                                                      // Creat the matching table of delta X_1
    for(int i=0;i<=255;i++){
        for(int j=0;j<=255;j++){
            for(int k=0;k<=255;k++){
                uint8_t key_guess[3]={i,j,k};
                uint8_t x1[15];
                for(int l=0;l<12;l++){
                    if(l%2==0) x1[l]=Compute_1(c[l/2],key_guess);
                    else x1[l]=Compute_1(cx[l/2],key_guess);
                }
                uint8_t delta[6];
                for(int l=0;l<6;l++){
                    delta[l]=x1[2*l]^x1[2*l+1];
                }
                uint64_t d=0;
                for(int n=0;n<6;n++){
                    d=(d << 8) | delta[n];                      
                }
                uint32_t ktp=0;
                ktp=i;
                ktp=(ktp<<8)|j;                                 
                ktp=(ktp<<8)|k;
                Delta_key_x_1.insert(make_pair(d,ktp));  
            }
        }
    }
}

uint8_t Compute_1(uint8_t ciphertext[16], uint8_t tweakey1[3]){                             //Compute the 1st cell from the ciphertext
    uint8_t tp[10];
    tp[0]=ciphertext[7]^ciphertext[11]^ciphertext[15];
    tp[1]=ciphertext[4]^ciphertext[12];
    tp[2]=ciphertext[13]^ciphertext[1];
    tp[0]^=tweakey1[1];
    for(int i=0;i<3;i++){
        tp[i]=Sinv[tp[i]];
    }
    tp[2]=tp[0]^tp[1]^tp[2];
    tp[2]^=tweakey1[0];
    tp[2]=Sinv[tp[2]];
    tp[2]^=tweakey1[2];
    tp[2]=Sinv[tp[2]];
    return tp[2];
}


uint8_t Compute_13( uint8_t ciphertext[16], uint8_t tweakey1[3]){                           //Compute the 13rd cell from the ciphertext
    uint8_t tp[10];
    tp[0]=ciphertext[7];
    tp[0]^=tweakey1[1];
    tp[0]=Sinv[tp[0]];

    tp[1]=ciphertext[2]^ciphertext[14];
    tp[1]=Sinv[tp[1]];
    tp[2]=tp[1]^tp[0];
    tp[2]=Sinv[tp[2]];

    tp[3]=ciphertext[5]^ciphertext[9]^ciphertext[13];
    tp[3]^=((RC[39] >> 4) & 0x3);
    tp[3]^=tweakey1[2];
    tp[3]=Sinv[tp[3]];
    tp[3]^=tweakey1[0];
    tp[3]^=(RC[38] & 0xf);
    tp[3]=Sinv[tp[3]];
    tp[3]^=tp[2];
    tp[3]=Sinv[tp[3]];
    return tp[3];
}

void mix_columns(uint8_t state[16])
{
    uint8_t tmp;
    for (uint8_t j = 0; j < 4; j++)
    {
        state[j + 4 * 1] ^= state[j + 4 * 2];
        state[j + 4 * 2] ^= state[j + 4 * 0];
        state[j + 4 * 3] ^= state[j + 4 * 2];
        tmp = state[j + 4 * 3];
        state[j + 4 * 3] = state[j + 4 * 2];
        state[j + 4 * 2] = state[j + 4 * 1];
        state[j + 4 * 1] = state[j + 4 * 0];
        state[j + 4 * 0] = tmp;
    }
}

void inv_mix_columns(uint8_t state[16])
{
    uint8_t tmp;
    for (uint8_t j = 0; j < 4; j++)
    {
        tmp = state[j + 4 * 3];
        state[j + 4 * 3] = state[j + 4 * 0];
        state[j + 4 * 0] = state[j + 4 * 1];
        state[j + 4 * 1] = state[j + 4 * 2];
        state[j + 4 * 2] = tmp;
        state[j + 4 * 3] ^= state[j + 4 * 2];
        state[j + 4 * 2] ^= state[j + 4 * 0];
        state[j + 4 * 1] ^= state[j + 4 * 2];
    }
}

void tweakey_schedule(int rounds, uint8_t tk[][16], uint8_t round_tweakey[][8])
{
    uint8_t tkp1[39][16];
    uint8_t tkp2[39][16];
    for (uint8_t i = 0; i < 16; i++)
        tk[0][i] = (tk[0][i] & 0xff);     
    for (uint8_t i = 0; i < 8; i++)
        round_tweakey[0][i] = tk[0][i];
    for (int r = 1; r < rounds; r++)
    {
        for (int i = 0; i < 16; i++)
        {
            tkp1[r - 1][i] = tk[r - 1][Q[i]];
        }
        for (int i = 0; i < 16; i++)
        {
            tk[r][i] = tkp1[r - 1][i];
        }
        for (int i = 0; i < 8; i++)
            round_tweakey[r][i] = tk[r][i];
    }
}

void enc(int R, uint8_t plaintext[16], uint8_t ciphertext[16], uint8_t tk[][8])
{
    for (uint8_t i = 0; i < 16; i++)
    {
        ciphertext[i] = plaintext[i] & 0xff;
    }
    for (uint8_t r = 0; r < R; r++)
    {
        // SBox
        for (uint8_t i = 0; i < 16; i++)
            ciphertext[i] = S[ciphertext[i]];
        // Add constants (constants only affects on three upper cells of the first column)
        ciphertext[0] ^= (RC[r] & 0xf);
        ciphertext[4] ^= ((RC[r] >> 4) & 0x3);
        ciphertext[8] ^= 0x2;
        // Add round tweakey (tweakey only exclusive-ored with two upper rows of the state)
        for (uint8_t i = 0; i < 8; i++)
            ciphertext[i] ^= tk[r][i];
        // Permute nibbles
        uint8_t temp[16];
        for (uint8_t i = 0; i < 16; i++)
            temp[i] = ciphertext[i];
        for (uint8_t i = 0; i < 16; i++)
            ciphertext[i] = temp[P[i]];
        // MixColumn
        mix_columns(ciphertext);
    }
}

void enc_e_32_13(int R, uint8_t plaintext[16], uint8_t ciphertext[16], uint8_t tk[][8], uint8_t e)
{
    for (uint8_t i = 0; i < 16; i++)
    {
        ciphertext[i] = plaintext[i] & 0xff;
    }
    for (uint8_t r = 0; r < R; r++)
    {
        if(r==31){
            ciphertext[13]^=e;
        }
        // SBox
        for (uint8_t i = 0; i < 16; i++)
            ciphertext[i] = S[ciphertext[i]];
        // Add constants (constants only affects on three upper cells of the first column)
        ciphertext[0] ^= (RC[r] & 0xf);
        ciphertext[4] ^= ((RC[r] >> 4) & 0x3);
        ciphertext[8] ^= 0x2;
        // Add round tweakey (tweakey only exclusive-ored with two upper rows of the state)
        for (uint8_t i = 0; i < 8; i++)
            ciphertext[i] ^= tk[r][i];
        // Permute nibbles
        uint8_t temp[16];
        for (uint8_t i = 0; i < 16; i++)
            temp[i] = ciphertext[i];
        for (uint8_t i = 0; i < 16; i++)
            ciphertext[i] = temp[P[i]];
        // MixColumn
        mix_columns(ciphertext);
    }
}

int main()
{   
    uint8_t tweakey1[16]={0x63,0xbe,0x39,0xe8,0x10,0xfa,0x7b,0xfa,0x12,0xf3,0x9b,0x7d,0x05,0x84,0x6b,0x6b};
    uint8_t p[6][16]=
    {{0x1f, 0xdd, 0x41, 0x6a, 0xba, 0x16, 0x12, 0x36, 0x24, 0x68, 0x9c, 0x62, 0x94, 0x55, 0xc5, 0xfa},
    {0xf, 0xf3, 0xe5, 0x37, 0x7b, 0xf9, 0x31, 0x2a, 0xbd, 0x3e, 0x68, 0xcc, 0xee, 0x17, 0x82, 0x2a},
    {0x6f, 0x96, 0xd4, 0xd9, 0x3f, 0xc9, 0x1, 0x66, 0x9c, 0x9a, 0x5, 0x1, 0x96, 0xe, 0x38, 0xcd},
    {0x70, 0x23, 0xd, 0x4e, 0xcd, 0x40, 0x5c, 0x74, 0x8a, 0x1e, 0xd5, 0xd1, 0xf6, 0x90, 0x18, 0xf2},
    {0xa0, 0x16, 0x94, 0x35, 0xd9, 0xfe, 0xeb, 0xc4, 0x1b, 0xab, 0x63, 0x25, 0x32, 0x2b, 0xf6, 0x56},
    {0xdf, 0x9b, 0x91, 0x7e, 0xab, 0xe, 0x8, 0xa1, 0x99, 0x14, 0x1f, 0xd6, 0x34, 0x82, 0xfb, 0x70}};
    uint8_t tk[40][16];    // intermediate variable for key schedule 
    uint8_t tk_es[40][16];    // intermediate variable for key schedule in exclusively search phrase
    int R = 40;         //round
    uint8_t rtk[40][8];     // round tweakey
    uint8_t rtk_es[40][8];    // round tweakey
    uint8_t c[6][16];       // storage ciphtext
    uint8_t cx[6][16];      // storage ciphtext with difference
    for (int i = 0; i < 16; i++)
    {
        tk[0][i] = tweakey1[i];
    }
    tweakey_schedule(R, tk, rtk);       
    uint8_t df =0xb2;       // set the difference injected
    for(int i=0;i<6;i++){
        enc(R, p[i], c[i], rtk);              //encrypt 
        enc_e_32_13(R,p[i],cx[i],rtk,df);     //encrypt with difference injected in the 13rd cell of the 32nd round.
    }
    Creat_Table_1(c, cx);                 // establish the matching table of Delta_X_1 
    Creat_Table_13(c, cx);                // establish the matching table of Delta_X_13 
    uint64_t tk_after_1 [1000][16];        // storage the remaining subkey cells guessed after filter 1
    long long num_1=0;                                                //number of remaining subkey cells after filter 1
    multimap<uint64_t, uint32_t>::iterator iter,n;
    for(n=Delta_key_x_1.begin();n!=Delta_key_x_1.end();n++) {                               // filter 1
        if((iter=Delta_key_x_13.find(n->first)) != Delta_key_x_13.end()){
        cout<<"First filter 13-1 got result "<<num_1+1<<". The remaining key is: ";
        tk_after_1[num_1][15]=(iter->second)&0xff;                                     // storage the remaining key after filter 1
        tk_after_1[num_1][10]=(iter->second>>8)&0xff;
        tk_after_1[num_1][3]=(iter->second>>16)&0xff;
        tk_after_1[num_1][13]=(n->second)&0xff;
        tk_after_1[num_1][9]=(n->second>>8)&0xff;
        tk_after_1[num_1][2]=(n->second>>16)&0xff;
        for(int j=0;j<16;j++){
            cout<<hex<<(int)tk_after_1[num_1][j]<<" ";                          
        }
        cout<<endl;num_1++;
        }
    }
    for(int i=0;i<4;i++){
        enc_e_32_15(R,p[i],cx[i],rtk,df);           // encrypt again with injecting difference in the 15th cell of the 32nd round
    }
    uint8_t tk_after_2 [1000][16];                  // storage subkey cells obtained after filter 2
    long long num_2=0;                              //number of remaining subkey cells after filter 2
    int range_1[6]={15,9,10,3,13,2};                // the location of the subkey cells guessed from last round
    for(int i=0;i<num_1;i++){
        uint8_t tk_15= tk_after_1[i][15];          //tk_15 and tk_9 are needed in the second filter
        uint8_t tk_9= tk_after_1[i][9];
        Creat_Table_3(c,cx, tk_15);               // establish the matching table of Delta_X_3 
        Creat_Table_15(c,cx, tk_9);               // establish the matching table of Delta_X_15 
        multimap<uint64_t, uint32_t>::iterator iter1,n1;
        for(n1=Delta_key_x_3.begin();n1!=Delta_key_x_3.end();n1++) {            // filter 2
            if((iter1=Delta_key_x_15.find(n1->first)) != Delta_key_x_15.end()){
            cout<<"Second filter 15-3 got result "<<num_2+1<<". The remaining key is: ";
            for(int &k: range_1){
                tk_after_2[num_2][k]=tk_after_1[i][k];                     // storage the remaining subkey cells guessed after filter 1
            }
            tk_after_2[num_2][7]=((iter1->second)>>8)&0xff;                // storage the remaining subkey cells guessed after filter 2
            tk_after_2[num_2][14]=(iter1->second)&0xff;
            tk_after_2[num_2][6]=(n1->second>>8)&0xff;
            tk_after_2[num_2][12]=(n1->second)&0xff;

            for(int j=0;j<16;j++){
                cout<<hex<<(int)tk_after_2[num_2][j]<<" ";                    
            }
            cout<<endl;num_2++;
            }
        }          
    }
    uint8_t tk_after_3 [1000][16];              // storage subkey cells obtained after filter 2
    long long num_3=0;                          //number of remaining subkey cells after filter 3
    int range_2[10]={3,10,15,2,9,13,7,14,6,12};         // the location of the subkey cells guessed from last round
    for(int i=0;i<num_2;i++){
        uint8_t tk_15= tk_after_2[i][15];               //tk_15, tk_6 and tk_13 are needed in the third filter
        uint8_t tk_6= tk_after_2[i][6];
        uint8_t tk_13= tk_after_2[i][13];
        Creat_Table_6(c, cx, tk_15, tk_6);        // establish the matching table of Delta_X_6 
        Creat_Table_14(c, cx, tk_13);             // establish the matching table of Delta_X_14
        multimap<uint64_t, uint32_t>::iterator iter1,n1;
        for(n1=Delta_key_x_6.begin();n1!=Delta_key_x_6.end();n1++) {            // filter 3
            if((iter1=Delta_key_x_14.find(n1->first)) != Delta_key_x_14.end()){
            cout<<"Third filter 14-6 got result "<<num_3+1<<". The remaining key is: ";
            for(int &x: range_2){
                tk_after_3[num_3][x]=tk_after_2[i][x];              // storage the remaining subkey cells guessed after filter 2
            }
            tk_after_3[num_3][8]=(iter1->second)&0xff;
            tk_after_3[num_3][5]=(iter1->second>>8)&0xff;           // storage the remaining subkey cells guessed after filter 3
            tk_after_3[num_3][11]=(n1->second)&0xff;
            for(int j=0;j<16;j++){
                cout<<hex<<(int)tk_after_3[num_3][j]<<" ";
            }
            cout<<endl;num_3++;
            }
        }
    }
    for(int m=0;m<16;m++) cx[1][m]=c[1][m];             //storage the correct ciphertext
    for(int i=0;i<256;i++){
        for(int j=0;j<256;j++){                         // Exclusively-Search phase
            for(int k=0;k<256;k++){
                for(int line=0;line<num_3;line++){          
                    tk_after_3[line][0]=i;
                    tk_after_3[line][1]=j;
                    tk_after_3[line][4]=k;
                    for(int m=0;m<16;m++) tk_es[0][m]=tk_after_3[line][m];
                    tweakey_schedule(R, tk_es, rtk_es);
                    enc(R, p[1], c[1], rtk_es);
                    int flag=1;
                    for(int m=0;m<16;m++){
                        if(c[1][m]!=cx[1][m])  flag=0; 
                    }
                    if(flag){
                        cout<<"The correct key is:   ";
                        for(int l=0;l<16;l++) 
                            cout<<hex<<(int)tweakey1[l]<<" ";
                        cout<<endl;
                        cout<<"The key recovered is: ";
                        for(int m=0;m<16;m++)
                            cout<<hex<<(int)tk_after_3[line][m]<<" ";
                        cout<<endl<<"The number of remaining subkey cells after first filter: "<<(int)num_1<<", second filter: "<<(int)num_2<<", third filter: "<<num_3<<"."<<endl;
                        abort();
                    }
                } 
            }
        }
    }
    cout<<"We failed to recover the key.";abort(); 
}