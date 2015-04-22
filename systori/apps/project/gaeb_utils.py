from lxml import objectify, etree

from ..task.models import Job, TaskGroup, Task, TaskInstance
from ..accounting.models import Account
from .models import Project

def get_text(element):
    concatenated = []
    print("-------------------------------------------")
    for idx, el in enumerate(element.getchildren()):
        print(el.tag)
        print(idx)
        if el.tag is el.getparent().Text:
            print("el.Text")
        #elif el.tag is el.getparent().TextComplement:
        #   print("el.Compl")
        else:
            print("hallo")


def item_info(item):
    print("item_info called")
    name = item.Description.CompleteText.OutlineText.OutlTxt.TextOutlTxt.p.span.text
    description = [get_text(el) for el in item.Description.CompleteText.DetailTxt]
    return name, description

def get(el, path, default=None, required=False, element_only=False):
    parts = path.split('.')
    if hasattr(el, parts[0]):
        el = getattr(el, parts[0])
        if len(parts) > 1:
            return get(el, '.'.join(parts[1:]), default, required, element_only)
        else:
            if element_only:
                return el
            else:
                return el.pyval
    else:
        return default

"""
 <GAEB xmlns="http://www.gaeb.de/GAEB_DA_XML/200407">
 <GAEB xmlns="http://www.gaeb.de/GAEB_DA_XML/200407">
 {http://www.gaeb.de/GAEB_DA_XML/200407}Qty

 <GAEB xmlns="http://www.gaeb.de/GAEB_DA_XML/DA83/3.2">
 
"""

def gaeb_import(file):
        tree = objectify.parse(file)
        GAEB_NS = tree.xpath('namespace-uri(.)')
        root = tree.getroot()
        label = root.PrjInfo.LblPrj
        project = Project.objects.create(name=label)
        try:
            first_job_no = int(root.Award.BoQ.BoQInfo.Name)-1
            project.job_offset = first_job_no if first_job_no >= 0 else 0
        except:
            pass

        for ctgy in root.Award.BoQ.BoQBody.BoQCtgy:
            job = Job.objects.create(name=" ".join(ctgy.LblTx.xpath(".//text()")), project=project)
            for grp in ctgy.BoQBody.BoQCtgy:
                taskgroup = TaskGroup.objects.create(name=" ".join(grp.LblTx.xpath(".//text()")), job=job)
                for item in grp.BoQBody.Itemlist.getchildren():
                    task = Task.objects.create(taskgroup=taskgroup)
                    task.qty = get(item, "Qty", default=0)
                    task.unit = get(item, "QU", default="INFO")
                    for text_node in item.Description.CompleteText.DetailTxt.getchildren():
                        for p in text_node.getchildren():
                            for child in p.getchildren():
                                if child.tag in "{{{ns}}}span".format(ns=GAEB_NS):
                                    task.description += " ".join(child.xpath(".//text()"))
                                elif child.tag in "{{{ns}}}image".format(ns=GAEB_NS):
                                    task.description += " !Bild im LV vorhanden!"
                    for text_node in item.Description.CompleteText.OutlineText.getchildren():
                        task.name = " ".join(text_node.xpath(".//text()"))
                    TaskInstance.objects.create(task=task, selected=True)
                    task.save()
                taskgroup.save()
            job.save()
        project.save()
        project.account = Account.objects.create(account_type=Account.ASSET, code=str(10000+project.id))
        project.save()
        return project
