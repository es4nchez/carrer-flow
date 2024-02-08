import csv
from peewee import *

db = SqliteDatabase('database.db')

class Student(Model):
    id = PrimaryKeyField()
    name = CharField()
    linkedin = CharField(null=True)

    class Meta:
        database = db

class Company(Model):
    id = PrimaryKeyField()
    name = CharField()
    email = CharField()
    entreprise = CharField(null=True)
    email2 = CharField(null=True)
    email3 = CharField(null=True)

    class Meta:
        database = db

class Offer(Model):
    id = PrimaryKeyField()
    company = ForeignKeyField(Company, backref='offers')
    title = CharField()

    class Meta:
        database = db

class StudentOffer(Model):
    student = ForeignKeyField(Student, backref='offers')
    offer = ForeignKeyField(Offer, backref='students')
    preference_order = IntegerField()

    class Meta:
        database = db
        indexes = (
            # Create a unique index on student/offer
            (('student', 'offer'), True),
        )


MODELS = {
    'Company': Company,
    'Student': Student,
    'Offer': Offer,
    'StudentOffer': StudentOffer,
}

FGKEYS = {
    'Offer': [('company', 'name')],
    'StudentOffer': [('student', 'name'), ('offer', 'title')],
}

def record_to_row(record):
    row = []
    for field in record._meta.sorted_fields:
        if isinstance(field, ForeignKeyField) and (field.name, field.rel_field.name) in FGKEYS[type(record).__name__]:
            # Replace the foreign key with a value from the related table
            related_value = getattr(getattr(record, field.name), field.rel_field.name)
            row.append(related_value)
        else:
            row.append(getattr(record, field.name))
    return row

def row_to_record(model, row):
    record = {}
    for field, value in zip(model._meta.sorted_fields, row):
        if isinstance(field, ForeignKeyField) and (field.name, field.rel_field.name) in FGKEYS[type(model).__name__]:
            # Replace the value with the corresponding foreign key
            related_model = field.rel_model
            related_record = related_model.get(**{field.rel_field.name: value})
            record[field.name] = related_record
        else:
            record[field.name] = value
    return record

def export_to_csv(model, filename):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        # Write the header
        writer.writerow(model._meta.sorted_field_names)
        # Write the data
        for record in model.select():
            row = record_to_row(record)
            writer.writerow(row)
            
# Import from CSV

def import_from_csv(model, filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            data = dict(zip(header, row))
            record, created = model.get_or_create(id=data['id'], defaults=data)
            if not created:
                for key, value in data.items():
                    setattr(record, key, value)
                record.save()