'''
Created on 2012-2-29

@author: lzz
'''

from . import states

class AsyncResult(object):
    """Query task state.
    """

    #: The task uuid.
    task_id = None

    #: The task result backend to use.
    backend = None

    def __init__(self, task_id, backend=None, task_name=None, app=None):
        self.task_id = task_id
        self.backend = backend
        self.task_name = task_name

    def forget(self):
        """Forget about (and possibly remove the result of) this task."""
        self.backend.forget(self.task_id)

    def revoke(self, connection=None, connect_timeout=None):
        """Send revoke signal to all workers.

        Any worker receiving the task, or having reserved the
        task, *must* ignore it.

        """
        self.app.control.revoke(self.task_id, connection=connection,
                                connect_timeout=connect_timeout)

    def get(self, timeout=None, propagate=True, interval=0.5):
        """Wait until task is ready, and return its result.

        .. warning::

           Waiting for tasks within a task may lead to deadlocks.
           Please read :ref:`task-synchronous-subtasks`.

        :keyword timeout: How long to wait, in seconds, before the
                          operation times out.
        :keyword propagate: Re-raise exception if the task failed.
        :keyword interval: Time to wait (in seconds) before retrying to
           retrieve the result.  Note that this does not have any effect
           when using the AMQP result store backend, as it does not
           use polling.

        :raises celery.exceptions.TimeoutError: if `timeout` is not
            :const:`None` and the result does not arrive within `timeout`
            seconds.

        If the remote call raised an exception then that exception will
        be re-raised.

        """
        return self.backend.wait_for(self.task_id, timeout=timeout,
                                                   propagate=propagate,
                                                   interval=interval)

    def wait(self, *args, **kwargs):
        """Deprecated alias to :meth:`get`."""
        return self.get(*args, **kwargs)

    def ready(self):
        """Returns :const:`True` if the task has been executed.

        If the task is still running, pending, or is waiting
        for retry then :const:`False` is returned.

        """
        return self.status in self.backend.READY_STATES

    def successful(self):
        """Returns :const:`True` if the task executed successfully."""
        return self.status == states.SUCCESS

    def failed(self):
        """Returns :const:`True` if the task failed."""
        return self.status == states.FAILURE

    def __str__(self):
        """`str(self) -> self.task_id`"""
        return self.task_id

    def __hash__(self):
        """`hash(self) -> hash(self.task_id)`"""
        return hash(self.task_id)

    def __repr__(self):
        return "<AsyncResult: %s>" % self.task_id

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.task_id == other.task_id
        return other == self.task_id

    def __copy__(self):
        return self.__class__(self.task_id, backend=self.backend)

    def __reduce__(self):
        if self.task_name:
            return (_unpickle_result, (self.task_id, self.task_name))
        else:
            return (self.__class__, (self.task_id, self.backend,
                                     None, self.app))

    @property
    def result(self):
        """When the task has been executed, this contains the return value.
        If the task raised an exception, this will be the exception
        instance."""
        return self.backend.get_result(self.task_id)

    @property
    def info(self):
        """Get state metadata.  Alias to :meth:`result`."""
        return self.result

    @property
    def traceback(self):
        """Get the traceback of a failed task."""
        return self.backend.get_traceback(self.task_id)

    @property
    def state(self):
        """The tasks current state.

        Possible values includes:

            *PENDING*

                The task is waiting for execution.

            *STARTED*

                The task has been started.

            *RETRY*

                The task is to be retried, possibly because of failure.

            *FAILURE*

                The task raised an exception, or has exceeded the retry limit.
                The :attr:`result` attribute then contains the
                exception raised by the task.

            *SUCCESS*

                The task executed successfully. The :attr:`result` attribute
                then contains the tasks return value.

        """
        return self.backend.get_status(self.task_id)

    @property
    def status(self):
        """Deprecated alias of :attr:`state`."""
        return self.state
BaseAsyncResult = AsyncResult  # for backwards compatibility.

class EagerResult(BaseAsyncResult):

    def __init__(self, task_id, ret_value, state, traceback=None):
        self.task_id = task_id
        self._result = ret_value
        self._state = state
        self._traceback = traceback

    def __reduce__(self):
        return (self.__class__, (self.task_id, self._result,
                                 self._state, self._traceback))

    def __copy__(self):
        cls, args = self.__reduce__()
        return cls(*args)

    def successful(self):
        """Returns :const:`True` if the task executed without failure."""
        return self.state == states.SUCCESS

    def ready(self):
        """Returns :const:`True` if the task has been executed."""
        return True

    def get(self, timeout=None, propagate=True, **kwargs):
        """Wait until the task has been executed and return its result."""
        if self.state == states.SUCCESS:
            return self.result
        elif self.state in states.PROPAGATE_STATES:
            if propagate:
                raise self.result
            return self.result

    def revoke(self):
        self._state = states.REVOKED

    def __repr__(self):
        return "<EagerResult: %s>" % self.task_id

    @property
    def result(self):
        """The tasks return value"""
        return self._result

    @property
    def state(self):
        """The tasks state."""
        return self._state

    @property
    def traceback(self):
        """The traceback if the task failed."""
        return self._traceback

    @property
    def status(self):
        """The tasks status (alias to :attr:`state`)."""
        return self._state