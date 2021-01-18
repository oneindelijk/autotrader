from django.db import models

# Create your models here.

class SettingsPage(models.Model):

    pageName = models.CharField('Parameter Name', max_length = 200)

    def __str__(self):
        return self.pageName

class Setting(models.Model):

    settingsPage = models.ForeignKey(SettingsPage, on_delete=models.CASCADE)
    settingsParameter = models.CharField('Parameter Name', max_length = 200)
    settingsValue = models.CharField('Value', max_length = 512, blank = True)
    settingsComment = models.TextField('Comment', blank = True)
    settingsIntValue = models.IntegerField('Integer Value', blank = True, null=True)
    settingsFloatValue = models.FloatField('Float Value', blank = True, null=True)
    settingsType = models.IntegerField('ValueType', default=1)

    def __str__(self):
        return '{}:{}'.format(self.settingsPage,self.settingsParameter)
    
class Parameter(models.Model):

    settingsPage = models.ForeignKey(SettingsPage, on_delete=models.CASCADE)
    settingsParameter = models.CharField('Parameter Name', max_length = 200)
    settingsValue = models.CharField('Value', max_length = 512, blank = True)
    settingsComment = models.TextField('Comment', blank = True)
    settingsIntValue = models.IntegerField('Integer Value', blank = True, null=True)
    settingsFloatValue = models.FloatField('Float Value', blank = True, null=True)
    settingsType = models.IntegerField('ValueType', default=1)

    def __str__(self):
        return '{}:{}'.format(self.settingsPage,self.settingsParameter)