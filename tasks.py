from functools import partial, wraps

from invoke import task, Collection, call

from symbolic_regression import all_problems


def task_factory(prob_name, prob_func):
    @task
    def symbolic_regression_task(ctx):
        print(prob_name)
    symbolic_regression_task.__name__ = prob_name
    return symbolic_regression_task


def all_tasks():
    ns = Collection()
    for i, (prob_name, prob_func) in enumerate(all_problems.items()):
        this_task = task_factory(prob_name, prob_func)
        ns.add_task(this_task, name="t{}".format(i))
    return ns


@task(pre=[call(t) for t in all_tasks().tasks.values()])
def run_all(ctx):
    print(len(all_problems))
    print("hello")

default = Collection()
default.add_task(run_all)
