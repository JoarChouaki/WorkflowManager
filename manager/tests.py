from django.test import TestCase
from .models import WorkFlow
# Create your tests here.

class WorkFlowCase(TestCase):

    def test_rename(self):
        workflow = WorkFlow.objects.create(nb_steps=0,name="First workflow")
        workflow.rename("WorkFlow")
        self.assertEqual("WorkFlow",workflow.name)

    def test_add_step(self):
        workflow = WorkFlow.objects.create(nb_steps=0,name="First workflow")
        workflow.add_step("Begin",1)
        self.assertEqual(workflow.nb_step,1)
