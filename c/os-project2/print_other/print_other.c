#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/sched/task.h>
#include <linux/rcupdate.h>
#include <linux/pid.h>
#include <linux/errno.h>
#include <linux/moduleparam.h>


static int pid = -1;
module_param(pid, int, 0444);
MODULE_PARM_DESC(pid, "PID of the process to inspect");


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


static int print_other_init(void) {
    struct task_struct *task;
    char name[TASK_COMM_LEN];
    unsigned int state;

    if (pid <= 0) {
        printk(KERN_ERR "print_other: supply a positive pid\n");
        return -EINVAL;
    }

    rcu_read_lock();
    task = pid_task(find_vpid(pid), PIDTYPE_PID);
    
    if (task == NULL) {
        rcu_read_unlock();
        printk(KERN_ERR "print_other: PID %d not found\n", pid);
        return -ESRCH;
    }

    while (task != NULL) {
        get_task_comm(name, task);
        state = READ_ONCE(task->__state);

        printk(KERN_INFO "print_other: name=%s pid=%d state=%s (%u)\n", name, task->pid, state_name(state), state);

        if (task->pid == 1 || task->pid == 0) {
                break;
        }

        task = rcu_dereference(task->real_parent);
    }

    rcu_read_unlock();
    return 0;
}


static void print_other_exit(void) {
    printk(KERN_INFO "print_other: unloaded\n");
}


module_init(print_other_init);
module_exit(print_other_exit);


MODULE_LICENSE("GPL");
