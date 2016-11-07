if not request.env.web2py_runtime_gae:
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    db = DAL('google:datastore+ndb')
    session.connect(request, response, db=db)
response.generic_patterns = ['*'] if request.is_local else []

from gluon.tools import *
auth=Auth(globals(),db)
auth.settings.hmac_key='sha512:f97d3f0c-b0da-4d3e-b49c-a7af7b397e1b'
auth.define_tables()                         # creates all needed tables
crud=Crud(globals(),db)                      # for CRUD helpers using auth
service=Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')
TASK_TYPES = ('Phone', 'Fax', 'Mail', 'Meet')

db.define_table('Patients',Field('Name', requires=IS_NOT_EMPTY()),Field('Phone', requires=IS_NOT_EMPTY()),Field('Ailment', requires=IS_NOT_EMPTY()),Field('Symptoms',requires=IS_NOT_EMPTY()),Field('Email',requires=IS_EMAIL()),Field('RegDate','date',requires=IS_DATE()),Field('AppointmentTime','time',requires=IS_TIME()))
if auth.is_logged_in():
   me=auth.user.id
else:
   me=None

db.define_table('Staff',Field('Name',requires=IS_NOT_EMPTY()),Field('Qualification',requires=IS_NOT_EMPTY()),Field('SpecialistIn',requires=IS_NOT_EMPTY()),Field('picture','upload'))

db.define_table('Medicines',Field('Name',requires=IS_NOT_EMPTY()),Field('Uses'))
