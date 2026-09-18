#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/sched/task.h>
#include <linux/rcupdate.h>
#include <linux/pid.h>
#include <linux/errno.h>
#include <linux/moduleparam.h>


/* This will accept a pid as read only as an argument to the module.
 * pid is initialized to -1 for error handling later
*/
static int pid = -1;
module_param(pid, int, 0444);
MODULE_PARM_DESC(pid, "PID of the process to inspect");


/* This function takes an unsigned integer as an argument
 * This function will return a char pointer
 * This function will map the process state number to the string representation
*/
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


/* This function takes no arguments
 * This function will return an int
 * This function will check for valid input then recursively inspect the pid and parent pids
*/
static int print_other_init(void) {
    struct task_struct *task;
    char name[TASK_COMM_LEN];
    unsigned int state;

    /* This is validating the PID sent as an argument is a valid PID */
    if (pid <= 0) {
        printk(KERN_ERR "print_other: supply a positive pid\n");
        return -EINVAL;
    }

    rcu_read_lock();

    /* This will find a specific pid instead of a process group or session and set it in task */
    task = pid_task(find_vpid(pid), PIDTYPE_PID);
    
    if (task == NULL) {
        rcu_read_unlock();
        printk(KERN_ERR "print_other: PID %d not found\n", pid);
        return -ESRCH;
    }

    /* Loop will iterate until all parent pids have been inspected */
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
