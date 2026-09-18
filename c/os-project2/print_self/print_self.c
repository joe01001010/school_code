#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/sched/task.h>
#include <linux/rcupdate.h>


static const char *state_name(unsigned int state) {
    if (state == TASK_RUNNING) {
        return "TASK_RUNNING";

    } else if (state == TASK_INTERRUPTIBLE) {
        return "TASK_INTERRUPTIBLE";

    } else if (state == TASK_UNINTERRUPTIBLE) {
        return "TASK_UNINTERRUPTIBLE";

    } else if (state == TASK_STOPPED) {
        return "TASK_STOPPED";

    } else if (state == TASK_TRACED) {
        return "TASK_TRACED";

    } else {
        return "STATE_NOT_DEFINED";

    }
}


static int print_self_init(void) {
    struct task_struct *task;
    char name[TASK_COMM_LEN];
    unsigned int state;

    rcu_read_lock();

    task = current;

    while (task != NULL) {
        get_task_comm(name, task);
        state = READ_ONCE(task->__state);

        printk(KERN_INFO "print_self: name=%s pid=%d state=%s (%u)\n", name, task->pid, state_name(state), state);

        if (task->pid == 1 || task->pid == 0) {
                break;
        }

        task = rcu_dereference(task->real_parent);
    }

    rcu_read_unlock();
    return 0;
}


static void print_self_exit(void) {
    printk(KERN_INFO "print_self: unloaded\n");
}


module_init(print_self_init);
module_exit(print_self_exit);


MODULE_LICENSE("GPL");
