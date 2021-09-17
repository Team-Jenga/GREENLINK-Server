# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Event(models.Model):
    event_id = models.IntegerField(primary_key=True)
    member = models.OneToOneField('Member', models.DO_NOTHING)
    event_title = models.CharField(max_length=45)
    event_location = models.CharField(max_length=45)
    event_reporting_date = models.DateField()
    event_views = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'event'


class EventDetail(models.Model):
    event = models.OneToOneField(Event, models.DO_NOTHING, primary_key=True)
    event_management = models.CharField(max_length=45, blank=True, null=True)
    event_period_start = models.DateField(blank=True, null=True)
    event_period_end = models.DateField(blank=True, null=True)
    event_url = models.CharField(max_length=45, blank=True, null=True)
    event_image_url = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_detail'


class Favorite(models.Model):
    favorite_id = models.IntegerField(primary_key=True)
    member = models.ForeignKey('Member', models.DO_NOTHING)
    event = models.ForeignKey(Event, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'favorite'


class Member(models.Model):
    member_id = models.CharField(primary_key=True, max_length=10)
    member_pw = models.CharField(max_length=45)
    member_name = models.CharField(max_length=45)
    member_nickname = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'member'


class MemberAdmin(models.Model):
    member = models.OneToOneField(Member, models.DO_NOTHING, primary_key=True)
    member_admin_position = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'member_admin'


class MemberUser(models.Model):
    member = models.OneToOneField(Member, models.DO_NOTHING, primary_key=True)
    member_user_birth = models.CharField(max_length=45, blank=True, null=True)
    member_user_phone = models.CharField(max_length=45, blank=True, null=True)
    member_user_email = models.CharField(max_length=45, blank=True, null=True)
    member_user_location = models.CharField(max_length=45, blank=True, null=True)
    member_user_num_of_family = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member_user'