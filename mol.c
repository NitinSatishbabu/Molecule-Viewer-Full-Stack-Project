#include "mol.h"

//This function sets the struct atom variables
void atomset( atom *atom, char element[3], double *x, double *y, double *z ){
    strcpy(atom->element, element);
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

//This function gets the values stored in atom variables
void atomget( atom *atom, char element[3], double *x, double *y, double *z ){
    strcpy(element, atom->element);
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}

//This function sets the struct bond variables
void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ){
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->atoms = *atoms;
    bond->epairs = *epairs;
    compute_coords(bond);
}

//This function gets the values stored in bond variables
void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ){
    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;
    *epairs = bond->epairs;
}

//This function allocates memory for a new molecule using malloc, and returns NULL if malloc fails
molecule *molmalloc( unsigned short atom_max, unsigned short bond_max ){
    molecule *newMol = malloc(sizeof(molecule));
    if(newMol == NULL){
        return NULL;
    }
    newMol->atom_max = atom_max;
    newMol->atom_no = 0;
    newMol->atoms = malloc(sizeof(atom) * atom_max);
    if(newMol->atoms == NULL){
        return NULL;
    }
    newMol->atom_ptrs = malloc(sizeof(atom *) * atom_max);
    if(newMol->atom_ptrs == NULL){
        return NULL;
    }

    newMol->bond_max = bond_max;
    newMol->bond_no = 0;
    newMol->bonds = malloc(sizeof(bond) * bond_max);
    if(newMol->bonds == NULL){
        return NULL;
    }
    newMol->bond_ptrs = malloc(sizeof(bond *) * bond_max);
    if(newMol->bond_ptrs == NULL){
        return NULL;
    }

    return newMol;
}

//This function copies the data from src molecule to copMol.
molecule *molcopy( molecule *src ){

    molecule *copMol = molmalloc(src->atom_max, src->bond_max);
    if(copMol == NULL){
        return NULL;
    }

    for(int i = 0; i < src->atom_no; i++){
        molappend_atom(copMol, &src->atoms[i]);
        if(i < src->bond_no){
            molappend_bond(copMol, &src->bonds[i]);
        }
    }

    return copMol;
}

//This functions frees the atoms, bonds and pointers
void molfree( molecule *ptr ){
    free(ptr->atom_ptrs);
    free(ptr->atoms);
    free(ptr->bond_ptrs);
    free(ptr->bonds);
    free(ptr);
}

//This function adds atom to molecule and uses realloc to increase memory if atom_no is equal to atom_max.
void molappend_atom( molecule *molecule, atom *atom ){

    if(molecule->atom_no == molecule->atom_max){
        if (molecule->atom_max == 0){
            molecule->atom_max = 1;
        }
        else {
            molecule->atom_max = molecule->atom_max * 2;
        }

        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);
        if(molecule->atoms == NULL){
            fprintf( stderr, "Realloc for molecule->atoms failed\n");
            exit(-1);
        }

        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom *) * molecule->atom_max);
        if(molecule->atom_ptrs == NULL){
            fprintf( stderr, "Realloc for molecule->atom_ptrs failed\n");
            exit(-1);
        }

        for(int i = 0; i < molecule->atom_max; i++){
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }
    }

    molecule->atoms[molecule->atom_no] = *atom;
    molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];
    molecule->atom_no++;
}

//This function adds bond to molecule and uses realloc to increase memory if bond_no is equal to bond_max.
void molappend_bond( molecule *molecule, bond *bond ){
    if(molecule->bond_no == molecule->bond_max){
        if (molecule->bond_max == 0){
            molecule->bond_max = 1;
        }
        else {
            molecule->bond_max = molecule->bond_max * 2;
        }

        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);
        if(molecule->bonds == NULL){
            fprintf( stderr, "Realloc for molecule->bonds failed\n");
            exit(-1);
        }
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond *) * molecule->bond_max);
        if(molecule->bonds == NULL){
            fprintf( stderr, "Realloc for molecule->bonds failed\n");
            exit(-1);
        }

        for(int i = 0; i < molecule->bond_max; i++){
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        }
    }

    molecule->bonds[molecule->bond_no] = *bond;
    molecule->bonds[molecule->bond_no].atoms = molecule->atoms;
    molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
    molecule->bond_no++;
}

//This function compares two atom'z values and returns a value respectively.
int compare_atom(const void *a1, const void *a2){
    double ret = 0.0;
    atom *at1 = *(atom **)a1;
    atom *at2 = *(atom **)a2;
    ret = at1->z - at2->z;

    if(ret > 0){
      return 1;
    }
    else if (ret < 0){
      return -1;
    }
    else{
      return 0;
    }
    }

//This function compares two atom'z average values and returns a value respectively.
// int compare_bond(const void *b1, const void *b2){
//     double to_ret = 0.0;
//     double bond1_avg = 0.0;
//     double bond2_avg = 0.0;
//     bond *bo1 = *(bond **)b1;
//     bond *bo2 = *(bond **)b2;
//     bond1_avg = (bo1->a1->z + bo1->a2->z) / 2;
//     bond2_avg = (bo2->a1->z + bo2->a2->z) / 2;
//     to_ret = bond1_avg - bond2_avg;
//     if(to_ret > 0){
//       return 1;
//     }
//     else if (to_ret < 0){
//       return -1;
//     }
//     else{
//       return 0;
//     }
//     }

//This function sorts atoms and bonds
void molsort( molecule *molecule ){

    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom *), compare_atom);
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond *), bond_comp);
}

//Defines the matrix
void xrotation( xform_matrix xform_matrix, unsigned short deg ){
    double rad = (deg * M_PI) / 180.0;
    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = -sin(rad);
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(rad);
    xform_matrix[2][2] = cos(rad);
}

//Defines the matrix
void yrotation( xform_matrix xform_matrix, unsigned short deg ){
    double rad = (deg * M_PI) / 180.0;
    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(rad);
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = -sin(rad);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(rad);
}

//Defines the matrix
void zrotation( xform_matrix xform_matrix, unsigned short deg ){
    double rad = (deg * M_PI) / 180.0;
    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = -sin(rad);
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = sin(rad);
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

//This function performs matrix multiplication
void mol_xform( molecule *molecule, xform_matrix matrix ){
    double temp_x = 0.0;
    double temp_y = 0.0;
    double temp_z = 0.0;

    for(int i = 0; i < molecule->atom_no; i++){
        temp_x = molecule->atoms[i].x;
        temp_y = molecule->atoms[i].y;
        temp_z = molecule->atoms[i].z;
        molecule->atoms[i].x = (matrix[0][0] * temp_x) +  (matrix[0][1] * temp_y) + (matrix[0][2] * temp_z);
        molecule->atoms[i].y = (matrix[1][0] * temp_x) +  (matrix[1][1] * temp_y) + (matrix[1][2] * temp_z);
        molecule->atoms[i].z = (matrix[2][0] * temp_x) +  (matrix[2][1] * temp_y) + (matrix[2][2] * temp_z);
    }

    for(int j = 0; j < molecule->bond_no; j++){
        compute_coords(&molecule->bonds[j]);
    }
}
//computing coordinates of bonds
void compute_coords( bond *bond ){
    atom *atom1 = &(bond->atoms[bond->a1]);
    atom *atom2 = &(bond->atoms[bond->a2]);

    bond->z = (atom1->z + atom2->z) / 2;

    bond->x1 = atom1->x;
    bond->y1 = atom1->y;
    bond->x2 = atom2->x;
    bond->y2 = atom2->y;

    double dif_x = atom2->x - atom1->x;
    double dif_y = atom2->y - atom1->y;
    bond->len = sqrt((dif_x * dif_x) + (dif_y * dif_y));
    bond->dx = dif_x / bond->len;
    bond->dy = dif_y / bond->len;

}
// comparing z values of bonds
int bond_comp( const void *a, const void *b ){
    double to_ret = 0.0;
    bond *bo1 = *(bond **)a;
    bond *bo2 = *(bond **)b;
    to_ret = bo1->z - bo2->z;
    if(to_ret > 0){
      return 1;
    }
    else if (to_ret < 0){
      return -1;
    }
    else{
      return 0;
    }
}
