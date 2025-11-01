from django.db import models


class Actions(models.Model):
    duration = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    name = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    title1 = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    title2 = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.CharField(max_length=160, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    titlenext = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    text = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    text2 = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    price = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    url = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    displayorder = models.PositiveIntegerField(blank=True, null=True, db_comment='Display order')

    class Meta:
        managed = False
        db_table = 'actions'


class Categories(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')

    class Meta:
        managed = False
        db_table = 'categories'


class Comptas(models.Model):
    date = models.DateField(blank=True, null=True)
    moyen = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True, db_comment='Moyen encaissement : Chèque, espèces, virement')
    categorie = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    label = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    labelbanque = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tiers = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    member_id = models.PositiveIntegerField(blank=True, null=True, db_comment='-> user')
    action = models.ForeignKey(Actions, models.DO_NOTHING, blank=True, null=True, db_comment='-> action')
    isbanqueok = models.PositiveIntegerField(db_column='isBanqueOk', blank=True, null=True)  # Field name made lowercase.
    ismilsabores = models.PositiveIntegerField(db_column='isMilSabores', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'comptas'


class Events(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    title1 = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    title2 = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    description = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    text = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    starttime = models.CharField(max_length=5, db_collation='utf8mb3_unicode_ci')
    enddate = models.DateField(blank=True, null=True)
    endtime = models.CharField(max_length=5, db_collation='utf8mb3_unicode_ci')
    location = models.ForeignKey('Locations', models.DO_NOTHING, blank=True, null=True, db_comment='-> Location')
    link = models.CharField(max_length=100, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    module_id = models.PositiveBigIntegerField(blank=True, null=True, db_comment='-> Module')
    orchestra = models.ForeignKey('Orchestras', models.DO_NOTHING, blank=True, null=True, db_comment='-> article (isGroup=1)')
    price = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    isevent = models.PositiveIntegerField(db_column='isEvent')  # Field name made lowercase.
    isdance = models.PositiveIntegerField(db_column='isDance')  # Field name made lowercase.
    dancetype = models.CharField(db_column='danceType', max_length=50, db_collation='utf8mb3_unicode_ci', blank=True, null=True)  # Field name made lowercase.
    istown = models.PositiveIntegerField(db_column='isTown')  # Field name made lowercase.
    islive = models.PositiveIntegerField(db_column='isLive')  # Field name made lowercase.
    isgroup = models.PositiveIntegerField(db_column='isGroup')  # Field name made lowercase.
    iscanceled = models.PositiveIntegerField(db_column='isCanceled')  # Field name made lowercase.
    isenabled = models.PositiveIntegerField(db_column='isEnabled')  # Field name made lowercase.
    datepublished = models.DateField(db_column='datePublished', blank=True, null=True)  # Field name made lowercase.
    datelastmodified = models.DateField(db_column='dateLastModified', blank=True, null=True)  # Field name made lowercase.
    author = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    canonicaleventid = models.PositiveIntegerField(db_column='canonicalEventId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'events'


class Locations(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    title2 = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    address = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    text = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    link = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    url = models.CharField(unique=True, max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locations'


class Members(models.Model):
    forname = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    name = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    instrument = models.CharField(max_length=45, db_collation='utf8mb3_bin', blank=True, null=True)
    email = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    phone = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    address = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    postalcode = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    town = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    lat = models.FloatField(blank=True, null=True, db_comment='latittude')
    lng = models.FloatField(blank=True, null=True, db_comment='longitude')
    description = models.TextField(db_collation='utf8mb3_bin', blank=True, null=True)
    url = models.CharField(max_length=255, db_collation='utf8mb3_bin', blank=True, null=True)
    noadhesion = models.IntegerField(db_column='noAdhesion', blank=True, null=True, db_comment='pour cartes adhérents')  # Field name made lowercase.
    username = models.CharField(max_length=50, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    password = models.CharField(max_length=60, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    role = models.CharField(max_length=20, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    isenabled = models.PositiveIntegerField(db_column='isEnabled')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'members'


class Orchestras(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    title1 = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    title2 = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    description = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    text = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    isworkshop = models.PositiveIntegerField(db_column='isWorkshop')  # Field name made lowercase.
    url = models.CharField(unique=True, max_length=255, db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    isenabled = models.PositiveIntegerField(db_column='isEnabled')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orchestras'