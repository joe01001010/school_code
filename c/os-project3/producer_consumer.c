#include <pthread.h>
#include <stdbool.h>
#include <stdio.h>


enum { CAPACITY = 12 };

char queue[CAPACITY];
int head, tail, count;
bool producer_done;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t not_empty = PTHREAD_COND_INITIALIZER;
pthread_cond_t not_full = PTHREAD_COND_INITIALIZER;


void enqueue(char c)
{
  pthread_mutex_lock(&lock);

  while (count == CAPACITY)
    pthread_cond_wait(&not_full, &lock);

  queue[tail] = c;
  tail = (tail + 1) % CAPACITY;
  count++;

  pthread_cond_signal(&not_empty);
  pthread_mutex_unlock(&lock);
}


int dequeue(void)
{
  pthread_mutex_lock(&lock);

  while (count == 0 && !producer_done)
    pthread_cond_wait(&not_empty, &lock);

  if (count == 0)
  {
    pthread_mutex_unlock(&lock);
    return EOF;
  }

  int c = queue[head];
  head = (head + 1) % CAPACITY;
  count--;

  pthread_cond_signal(&not_full);
  pthread_mutex_unlock(&lock);
  return c;
}


void *producer(void *arg)
{
  FILE *input = arg;
  int c;

  while ((c = fgetc(input)) != EOF)
    enqueue((char) c);

  pthread_mutex_lock(&lock);
  producer_done = true;
  pthread_cond_signal(&not_empty);
  pthread_mutex_unlock(&lock);
  return NULL;
}


void *consumer(void *arg)
{
  (void)arg;
  int c;

  while ((c = dequeue()) != EOF)
    putchar(c);

  return NULL;
}


int main(int argc, char *argv[])
{
  // Read file and instantiate the producer and consumer threads
  FILE *input = fopen("message.txt", "r");
  pthread_t producer_thread, consumer_thread;

  // Create the threads for producer and consumer
  pthread_create(&producer_thread, NULL, producer, input);
  pthread_create(&consumer_thread, NULL, consumer, NULL);

  // Wait for the threads to finish
  pthread_join(producer_thread, NULL);
  pthread_join(consumer_thread, NULL);

  // Close silly lil file when its no longer in use
  fclose(input);

  return 0;
}
