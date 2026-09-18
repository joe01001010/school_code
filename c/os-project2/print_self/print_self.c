#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/sched/task.h>
#include <linux/rcupdate.h>


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
 * This function will return an integer
 * This function will take the *task which points to the kernel task record
 * Uses the defined TASK_COMM_LEN for the char array
 * state will be the unsigned integer that represents the process's state
 * As the function traverses the PIDs to the parent pid rcu_read_lock() will protext the records from being freed
*/
static int print_self_init(void) {
    struct task_struct *task;
    char name[TASK_COMM_LEN];
    unsigned int state;

    rcu_read_lock();

    task = current;

    /* This will start at the current task and iterate until the task is NULL or if the task->pid is 0 or 1 */
    while (task != NULL) {
        /* This is copying the task's name into the name variable */
        get_task_comm(name, task);

        /* This is reading the task's scheduling state once so the compiler doesnt interpret repeated access */
        state = READ_ONCE(task->__state);

        printk(KERN_INFO "print_self: name=%s pid=%d state=%s (%u)\n", name, task->pid, state_name(state), state);

        if (task->pid == 1 || task->pid == 0) {
                break;
        }

        /* This is incrementing the current task to the parent task so the loop will eventually reach PID 1 or PID 0 */
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
