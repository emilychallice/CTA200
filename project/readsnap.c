#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

float **readparticlepositions(const char *filename) {
	unsigned int a;
	FILE *fp;
	fp = fopen(filename, "rb");

	unsigned int blocksize;
	float x;
	int npart[6];  /* [0]gas, [1]halo, [2]disk, [3]bulge, [4]stars, [5]bndry */

	// header
	fread(&blocksize, sizeof(uint32_t), 1, fp);
	fread(npart, sizeof(uint32_t), 6, fp);
	fseek(fp, blocksize + sizeof(uint32_t), SEEK_SET);
	fread(&blocksize, sizeof(uint32_t), 1, fp);

	float *gas = malloc(npart[0]*3*sizeof(float));
	float *halo = malloc(npart[1]*3*sizeof(float));
	float *disk = malloc(npart[2]*3*sizeof(float));
	float *bulge = malloc(npart[3]*3*sizeof(float));
	float *stars = malloc(npart[4]*3*sizeof(float));
	float *bndry = malloc(npart[5]*3*sizeof(float));

	float **particles = malloc(6*sizeof(float*));
	particles[0] = gas;
	particles[1] = halo;
	particles[2] = disk;
	particles[3] = bulge;
	particles[4] = stars;
	particles[5] = bndry;

	// particle positions
	fread(&blocksize, sizeof(uint32_t), 1, fp);
	printf("%u\n",blocksize);

	fread(halo, sizeof(float), npart[0]*3, fp);
	fread(halo, sizeof(float), npart[1]*3, fp);
	fread(disk, sizeof(float), npart[2]*3, fp);
	fread(bulge, sizeof(float), npart[3]*3, fp);
	fread(stars, sizeof(float), npart[4]*3, fp);
	fread(bndry, sizeof(float), npart[5]*3, fp);

	fread(&blocksize, sizeof(uint32_t), 1, fp);

	// particle velocities
	fread(&blocksize, sizeof(uint32_t), 1, fp);

	// ... etc ... for anything else needed from the file
	//printf("%u\n",blocksize);

	fclose(fp);

	return particles;
}

int main() {
	readparticlepositions("snapshot_001");
	return 0;
}
