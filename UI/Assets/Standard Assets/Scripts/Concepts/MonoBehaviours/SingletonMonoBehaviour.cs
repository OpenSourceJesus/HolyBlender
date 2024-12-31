using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class SingletonMonoBehaviour<T> : MonoBehaviour where T : MonoBehaviour
{
	public static T instance;
	public static T Instance
	{
		get
		{
			if (instance == null)
				instance = FindObjectOfType<T>();
			return instance;
		}
	}
	public MultipleInstancesHandlingType handleMultipleInstances;
	public bool persistant;
	
	public virtual void Awake ()
	{
#if UNITY_EDITOR
		if (!Application.isPlaying)
			return;
#endif
		if (Instance != this && handleMultipleInstances != MultipleInstancesHandlingType.KeepAll)
		{
			if (handleMultipleInstances == MultipleInstancesHandlingType.DestroyNew)
			{
				Destroy(gameObject);
				return;
			}
			else
				Destroy(instance.gameObject);
		}
		if (persistant)
			DontDestroyOnLoad(gameObject);
	}

	public enum MultipleInstancesHandlingType
	{
		KeepAll,
		DestroyNew,
		DestroyOld
	}
}