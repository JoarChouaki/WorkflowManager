from django.db import models
from .utils import check_type

# Create your models here.

class WorkFlow(models.Model):
    """

    A WorkFlow is represented as several ordered steps (it can be empty as well).
    It can be name and renamed by the user.

    """
    nb_steps = models.IntegerField(default=0)
    name = models.CharField(max_length=200,default='New workflow')

    def __str__(self):
        return self.name + ' - ' + str(self.nb_steps) + ' steps' 

    def add_step(self,status,index):
        """
        Insert a step into the workflow at the position 'index'.
        """
        check_type(index,int)
        if index < 0 or index > self.nb_steps + 1:
            raise ValueError('Cannot insert a step in Workflow ',self,' at index ',index)

        next_steps = Step.objects.filter(number__gte=index)
        for step in next_steps:
            step.number += 1
            step.save()
        self.nb_steps += 1
        self.save()
        return Step.objects.create(workflow=self,status=status,number=index)


    def del_step(self,step_to_delete):
        """
        Delete the input step from the workflow, provided that this step belongs to this WorkFlow.
        """
        check_type(step_to_delete,Step)
        if step_to_delete.workflow.pk != self.pk:
            raise AttributeError('This step does not belong to this workflow')
        next_steps = Step.objects.filter(number__gt=step_to_delete.number)
        for step in next_steps:
            step.number -= 1
            step.save()
        self.nb_steps -= 1

        self.save()
        step_to_delete.delete()

    def rename(self,new_name):
        check_type(new_name,str)
        self.name = new_name
        self.save()

class Step(models.Model):
    """
    
    Steps mark the progression of the projects in a given workflow.
    They are indexed starting from 1 and can be named by the user.

    """
    name = models.CharField(max_length=200,default='')
    workflow = models.ForeignKey(WorkFlow, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    number = models.IntegerField(default=1)

    def __str__(self):
        return 'Step n° ' + self.number + ' : ' + self.name + ' from workflow ' + self.workflow.name + ' - status = ' + self.status

    def add_entity(self,entity):
        check_type(entity,Entity)
        return Entity.objects.create(step=self)

    def del_entity(self,entity):
        check_type(entity,Entity)
        entity.delete()

    def change_status(self,new_status):
        check_type(new_status,string)
        self.status = new_status
        self.save()

    def rename(self,new_name):
        check_type(new_name,str)
        self.name = new_name
        self.save()


class Entity(models.Model):
    """

    An Entity can be a Project, or a simple Object. It's always link to a given Step from a WorkFlow.

    """
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    name = models.CharField(max_length=200) 
    class Meta:
        abstract = True

    def change_step(self,new_step):
        """
        Any entity can switch from a Step to another, even if they don't belong to the same WorkFlow.
        """
        check_type(new_step,Step)
        self.step = new_step
        self.save()


class Project(Entity):
    """

    This class allows the user to represent their projects. A Project is associated to a certain Step of a WorkFlow.
    It can contain Objects.

    """
    pass

class Object(Entity):
    """

    An Object allows the user to insert files (graphic charts, videos, pictures,...) in a given WorkFlow.
    It may be part of a Project.

    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')

