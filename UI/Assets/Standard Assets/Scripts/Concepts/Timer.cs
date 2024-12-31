using System;
using HolyBlender;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

[Serializable]
public class Timer
{
	public float duration;
	public float timeRemaining;
	float timeElapsed;
	public float TimeElapsed
	{
		get
		{
			return timeElapsed;
		}
	}
	public bool loop;
	public delegate void OnFinished (params object[] args);
	public event OnFinished onFinished;
	public object[] args;
	Coroutine timerRoutine;
	public bool realtime;
	public bool autoStopIfNotLooping = true;
	// public static List<Timer> runningInstances = new List<Timer>();

	public virtual void Start ()
	{
		if (timerRoutine == null)
			timerRoutine = GameManager.Instance.StartCoroutine(TimerRoutine ());
	}

	public virtual void Stop ()
	{
		if (timerRoutine != null)
		{
			GameManager.Instance.StopCoroutine(timerRoutine);
			timerRoutine = null;
			// runningInstances.Remove(this);
		}
	}

	public virtual IEnumerator TimerRoutine ()
	{
		// runningInstances.Add(this);
		bool justEnded;
		while (true)
		{
			justEnded = false;
			if (realtime)
			{
				timeRemaining -= Time.unscaledDeltaTime;
				timeElapsed += Time.unscaledDeltaTime;
			}
			else
			{
				timeRemaining -= Time.deltaTime;
				timeElapsed += Time.deltaTime;
			}
			while (timeRemaining <= 0)
			{
				yield return new WaitForEndOfFrame();
				if (onFinished != null)
					onFinished (args);
				if (loop)
					timeRemaining += duration;
				else if (autoStopIfNotLooping)
					Stop ();
				justEnded = true;
			}
			if (!justEnded)
				yield return new WaitForEndOfFrame();
		}
	}

	public virtual void Reset ()
	{
		Stop ();
		timeRemaining = duration;
		timeElapsed = 0;
	}
}
