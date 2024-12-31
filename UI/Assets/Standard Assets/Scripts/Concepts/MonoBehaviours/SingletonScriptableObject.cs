using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class SingletonScriptableObject<T> : ScriptableObject where T : ScriptableObject
{
	public static T instance;
	
	public virtual void Start ()
	{
		instance = this as T;
	}
	
	public static T GetInstance ()
	{
		if (instance == null)
			instance = FindObjectOfType<T>();
		return instance;
	}
}
