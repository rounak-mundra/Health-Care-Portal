from gluon.tools import Mail
mail = Mail()
mail.settings.server = 'research.iiit.ac.in:25'
mail.settings.sender = 'docters@iiit.ac.in'
def index():
    response.flash=T('WELCOME TO IIIT-H HEALTH CENTRE')
    x='AAROGYA'
    return locals()
@auth.requires_membership('doctors')
def Display():
    pics=SQLFORM.grid(db.Staff)
    return locals()
@auth.requires_login()
def Display1():
    pics=db().select(db.Staff.ALL)
    return locals()
@auth.requires_membership('doctors')
def Medicines():
    med=SQLFORM.grid(db.Medicines)
    return locals()
@auth.requires_login()
def Medicines1():
    med=db().select(db.Medicines.ALL)
    return locals()
@auth.requires_login()
def Registration_Form():
    form=SQLFORM(db.Patients).process()
    if form.accepted:
        response.flash='Form Accepted'
    elif form.errors:
        response.flash='Form has errors'
    else:
        response.flash='Please fill out the form'
    return dict(form=form)
@auth.requires_login()
def Search():
    return dict(form=FORM(INPUT(_id='keyword',_name='keyword',
    _onkeyup="ajax('callback', ['keyword'], 'target');")),
    target_div=DIV(_id='target'))

def callback():
    query = db.Patients.Name.contains(request.vars.keyword)
    pages = db(query).select(orderby=db.Patients.Name)
    links = [A(p.Name, _href=URL('Appointments_Booked',args=p.id)) for p in pages]
    return UL(*links)

def Show():
    return locals()
@auth.requires_login()
def Equipments():
    response.flash = "General Information"
    return locals()
@auth.requires_login()
def Appointments_Booked():
    rows=db().select(db.Patients.ALL)
    return locals()
@auth.requires_membership('doctors')
def Sending_Email():
    rows=db(db.Patients.id>0).select()
    for row in rows:
        x=row.Email
        mail.send(to=[x],
                  subject='Appointment Time',
           message="Dear Patient,\nYour appointment has been fixed. Kindly see the updated appointment time on the Health Portal.\n")
    return locals()
@auth.requires_membership('doctors')
def Manager():
    grid= SQLFORM.grid(db.Patients)
    return locals()
#@auth.requires_login()
#def Email_sending():
#    response.flash='email sending'
#    rows=db(db.Patients.id>0).select()
#    for row in rows:
#            db.queue.insert(status='pending',
#                            email=row.Email,
#                            subject='Appointment Time',
#                            msg='i m sorry')
#   while True:
 #       rows=db(db.queue.status=='pending').select()
    #for row in rows:
#            if mail.send(to=row.email,
 #                        subject=row.subject,
#                         message=row.msg):
 #               row.update_record(status='sent')
           # else:
            #    row.update_record(status='failed')
            #db.commit()

@auth.requires_login()
def edit_task():
    task_id=request.args(0)
    task=db.task[task_id] or redirect(error_page)
    person=db.person[task.person]
    db.task.person.writable=db.task.person.readable=False
    form=crud.update(db.task,task,next='view_task/[id]')
    return dict(form=form, person=person)

@auth.requires_login()
def view_task():
    task_id=request.args(0)
    task=db.task[task_id] or redirect(error_page)
    person=db.person[task.person]
    db.task.person.writable=db.task.person.readable=False
    form=crud.read(db.task,task)
    return dict(form=form, person=person, task=task)

@auth.requires_login()
def list_tasks():
    person_id=request.args(0)
    person=db.person[person_id]
    if person_id:
       tasks=db(db.task.person==person_id)\
               (db.task.created_by==auth.user.id)\
               (db.task.start_time>=request.now).select()
    else:
       tasks=db(db.task.created_by==auth.user.id)\
               (db.task.start_time<=request.now).select()
    db.task.person.default=person_id
    db.task.person.writable=db.task.person.readable=False
    form=crud.create(db.task,next='view_task/[id]')
    return dict(tasks=tasks,person=person,form=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
