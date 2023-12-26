create database med_vet;
use med_vet;
CREATE TABLE Diagnosticos (
    Diagnostico VARCHAR(255),
    Eritrocitos DOUBLE,
    Hemoglobina DOUBLE,
    Hematocrito DOUBLE,
    HCM DOUBLE,
    VGM DOUBLE,
    CHGM DOUBLE,
    Metarrubricitos DOUBLE,
    Proteina_Plasmatica DOUBLE,
    Leucocitos DOUBLE,
    Leucograma DOUBLE,
    Segmentados DOUBLE,
    Bastonetes DOUBLE,
    Blastos DOUBLE,
    Metamielocitos DOUBLE,
    Mielocitos DOUBLE,
    Linfocitos DOUBLE,
    Monocitos DOUBLE,
    Eosinofilos DOUBLE,
    Basofilos DOUBLE,
    Plaquetas DOUBLE
);
SELECT * FROM Diagnosticos;