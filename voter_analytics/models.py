from django.db import models

# Create your models here.
class Voter(models.Model):
    '''
    Store/represent the data from one voter.
    '''

    # identification
    voter_id = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.TextField()
    dob = models.DateField()
    dor = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.IntegerField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()
 
    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.voter_id} {self.first_name} {self.last_name}'

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    filename = 'newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers

    for line in f:
        fields = line.split(',')
       
        try:
            # create a new instance of Result object with this record from CSV
            voter = Voter(
                voter_id=fields[0].strip(),
                first_name=fields[1].strip(),
                last_name=fields[2].strip(),
                street_number=fields[3].strip(),
                street_name=fields[4].strip(),
                apartment_number=fields[5].strip(),
                zip_code=fields[6].strip(),
                dob=fields[7].strip(),
                dor=fields[8].strip(),
                party_affiliation=fields[9].strip(),
                precinct_number=int(fields[10].strip()),
                v20state=fields[11].strip() in ['True', 'true', '1'],
                v21town=fields[12].strip() in ['True', 'true', '1'],
                v21primary=fields[13].strip() in ['True', 'true', '1'],
                v22general=fields[14].strip() in ['True', 'true', '1'],
                v23town=fields[15].strip() in ['True', 'true', '1'],
                voter_score=int(fields[16].strip()),
            )
        
            voter.save() # commit to database
            
        except:
            print(f"Skipped: {fields}")
    
    print(f'Done. Created {len(Voter.objects.all())} Results.')
