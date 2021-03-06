# PylonsTemplates

*PylonsTemplates gives you additional paster templates for Pylons applications.*

Once the PylonsTemplates module is installed, you can create new Pylons
projects like this:

    paster create -t <templatename> <projectname>

## pylons_repoze_what

By [countergram (Jason Stitt)](http://github.com/countergram)

Based on the default Pylons paster template, the pylons_repoze_what template
implements a working authorization system based on repoze.what and
repoze.what-quickstart. (Authentication by repoze.who is automatically set
up as well.) The template generates:

* User, Group and Permission models for SQLALchemy
* A login (& logout) controller
* A minimal template for the login form.
* A package dependency on repoze.what-pylons, which includes decorators
  you can use on controllers and actions.
* Commented out sample code in websetup.py that creates a user, group,
  and permission.

### MORE DOCUMENTATION

* [http://what.repoze.org/docs/1.x/](http://what.repoze.org/docs/1.x/)
* [http://code.gustavonarea.net/repoze.what-pylons/](http://code.gustavonarea.net/repoze.what-pylons/)

### QUICK EXAMPLE OF REPOZE.WHAT-PYLONS USAGE

    from repoze.what.predicates import has_permission
    from repoze.what.plugins.pylonshq import ActionProtector

    class HelloWorldController(BaseController):
        @ActionProtector(has_permission('be_cool'))
        def index(self):
            return 'Hello World'


## pylons_cleaner_default

By [shazow (Andrey Petrov)](http://github.com/shazow)

Based on the default Pylons paster template, but contains some refactored
imports and additional example cases.

For SQLAlchemy:

* Import Session object directly, instead of accessing it through meta.Session
* Declarative object definition example

### QUICK EXAMPLES

One option...

    from myproject.model import Session, Foo

    class MyController(BaseController):
        def index(self):
            return Session.query(Foo).all()

More reasonable...

    from myproject import model
    Session = model.Session # Optional (if you don't like typing model.Session)
    engine = Session.bind # Optional (if you need the engine)

    ## Instead of:
    # from myproject.model import meta
    # Session = meta.Session

    class MyController(BaseController):
        def index(self):
            return Session.query(model.Foo).all()

Also works in `paster shell` and unit tests!
