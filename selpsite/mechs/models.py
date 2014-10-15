from django.db import models

class Attack(models.Model):
  def __unicode__(self):
    return self.name
  name = models.CharField(max_length=200)
  damage = models.IntegerField(default=0)

class StdMech(models.Model):
  def __unicode__(self):
    return self.name
  name = models.CharField(max_length=200)
  attackA = models.ForeignKey(Attack, related_name='attackA')
  attackB = models.ForeignKey(Attack, related_name='attackB', blank=True)
  attackC = models.ForeignKey(Attack, related_name='attackC', blank=True)

