#define sbi(var,bit)	(var) |= (1 << (bit))
#define cbi(var,bit)	(var) &= ~(1 << (bit))
#define tbi(var,bit)	(var) ^= (1 << (bit))
