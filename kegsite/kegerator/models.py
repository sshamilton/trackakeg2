from django.db import models

class Keg(models.Model):
    kegweight = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    kegempty = 712
    kegfull = 860
    kegtotal = kegfull-kegempty
    def currentvalue(self):
        cv = Keg.objects.order_by('-created_at')[:1]
        return cv.first().kegweight

    def percent(self):
        kegvalue = self.currentvalue() - self.kegempty
        return (round(kegvalue/self.kegtotal * 100))

    def pints(self):
        return (round(40.0*self.percent()/100.0))
