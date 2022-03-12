from django.db import models

# Create your models here.

class Adherent(models.Model):
    id = models.BigAutoField(primary_key=True)
    codeadh = models.CharField(unique=True, max_length=10)
    nomadh = models.CharField(max_length=100)
    prenomadh = models.CharField(max_length=100)
    datenaiss = models.DateField(blank=True, null=True)
    lieunaiss = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adherent'


class Benevole(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombene = models.CharField(max_length=100)
    prenombene = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'benevole'
        unique_together = (('nombene', 'prenombene'),)


class Decaissement(models.Model):
    id = models.BigAutoField(primary_key=True)
    numtrans = models.CharField(unique=True, max_length=10)
    datetrans = models.DateField()
    naturedep = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'decaissement'


class Document(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom_document = models.CharField(unique=True, max_length=200)
    document_type = models.ForeignKey('DocumentType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'document'


class DocumentEmpreint(models.Model):
    id = models.BigAutoField(primary_key=True)
    adherent = models.ForeignKey(Adherent, models.DO_NOTHING)
    document = models.ForeignKey(Document, models.DO_NOTHING)
    date_empreint = models.DateField(blank=True, null=True)
    rendu = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'document_empreint'


class DocumentType(models.Model):
    id = models.BigAutoField(primary_key=True)
    type_document = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'document_type'


class Encaissement(models.Model):
    id = models.BigAutoField(primary_key=True)
    numtrans = models.CharField(unique=True, max_length=10)
    datetrans = models.DateField()
    sourceenc = models.CharField(max_length=100)
    adherent = models.ForeignKey(Adherent, models.DO_NOTHING)
    montant = models.DecimalField(max_digits=65535, decimal_places=65535)

    class Meta:
        managed = False
        db_table = 'encaissement'


class Evenement(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom_evenement = models.CharField(unique=True, max_length=100)
    evenement_type = models.ForeignKey('EvenementType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'evenement'


class EvenementParticipation(models.Model):
    id = models.BigAutoField(primary_key=True)
    adherent = models.ForeignKey(Adherent, models.DO_NOTHING)
    evenement = models.ForeignKey(Evenement, models.DO_NOTHING)
    cancelled = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'evenement_participation'


class EvenementType(models.Model):
    id = models.BigAutoField(primary_key=True)
    type_evenement = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'evenement_type'


class Formation(models.Model):
    id = models.BigAutoField(primary_key=True)
    codeforma = models.CharField(unique=True, max_length=100)
    nomform = models.CharField(max_length=100)
    desform = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'formation'


class FormationSalles(models.Model):
    id = models.BigAutoField(primary_key=True)
    codesalle = models.CharField(unique=True, max_length=100)
    nomsalle = models.CharField(max_length=100)
    capacitesalle = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'formation_salles'


class FormationSession(models.Model):
    id = models.BigIntegerField(primary_key=True)
    codesession = models.CharField(unique=True, max_length=100)
    datesession = models.DateField()
    formation = models.ForeignKey(Formation, models.DO_NOTHING)
    benevole = models.ForeignKey(Benevole, models.DO_NOTHING)
    formation_salle = models.ForeignKey(FormationSalles, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'formation_session'


class FormationSessionInscription(models.Model):
    id = models.BigAutoField(primary_key=True)
    formation_session = models.ForeignKey(FormationSession, models.DO_NOTHING)
    adherent = models.ForeignKey(Adherent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'formation_session_inscription'


class Sallemachine(models.Model):
    id = models.BigAutoField(primary_key=True)
    codesallem = models.CharField(unique=True, max_length=100)
    nomsallem = models.CharField(max_length=100)
    capacitesallem = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sallemachine'


class SallemachineReservation(models.Model):
    id = models.BigAutoField(primary_key=True)
    creneau = models.CharField(max_length=100)
    date_creneau = models.DateField()
    adherent = models.ForeignKey(Adherent, models.DO_NOTHING)
    sallemachine = models.ForeignKey(Sallemachine, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sallemachine_reservation'
        unique_together = (('creneau', 'date_creneau', 'sallemachine'),)
