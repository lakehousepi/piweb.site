from django.db import models

class TempSeries(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return u'%s' % self.name

class TempReading(models.Model):
    TEMP_SCALE_CHOICES = (
        ('F', 'Farenheit'),
        ('C', 'Centigrade'),
        ('K', 'Kelvin'),
    )
    
    tempseries = models.ForeignKey('TempSeries')
    timestamp = models.DateTimeField()
    value = models.FloatField()
    scale = models.CharField(max_length=1, choices=TEMP_SCALE_CHOICES)
    
    class Meta:
        unique_together = (
            ('tempseries', 'timestamp'),
        )
        
    @property
    def tempdict(self):
        td = {}
        if self.scale == 'F':
            td['F'] = self.value
            td['C'] = (self.value - 32.0) * (100.0/180.0)
            td['K'] = td['C'] + 273.15
        elif self.scale == 'C':
            td['C'] = self.value
            td['K'] = td['C'] + 273.15
            td['F'] = (td['C'] * (180.0/100.0)) + 32.0
        else:
            td['K'] = self.value
            td['C'] = td['K'] - 273.15
            td['F'] = (td['C'] * (180.0/100.0)) + 32.0
        return td
    
    def __unicode__(self):
        selfstring = u'%(tempseries)s=%(value)s%(scale)s@%(timestamp)s' % {
            'tempseries': self.tempseries.name,
            'value': self.value,
            'scale': self.scale,
            'timestamp': self.timestamp.strftime('%Y%m%d %H:%M:%S')
        }
        return selfstring

class IPSeries(models.Model):
    name = name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return u'%s' % self.name

class IPReading(models.Model):
    ipseries = models.ForeignKey('IPSeries')
    timestamp = models.DateTimeField()
    value = models.IPAddressField()
    
    class Meta:
        unique_together = (
            ('ipseries', 'timestamp'),
        )
    
    def __unicode__(self):
        selfstring = u'%(ipseries)s=%(value)s@%(timestamp)s' % {
            'ipseries': self.ipseries.name,
            'value': self.value,
            'timestamp': self.timestamp.strftime('%Y%m%d %H:%M:%S')
        }
        return selfstring