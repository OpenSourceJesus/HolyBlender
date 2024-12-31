/*
	This file defines a GameObject that can be temporarily and locally activated
*/

using System;
using HolyBlender;
using Extensions;
using UnityEngine;
using System.Collections;

[Serializable]
public class TemporaryActiveGameObject
{
	public GameObject obj;
	public float duration;
	public bool realtime;

	public virtual void Do ()
	{
		GameManager.updatables = GameManager.updatables.Add(new DoUpdater(this));
	}

	public class DoUpdater : IUpdatable
	{
		public TemporaryActiveGameObject temporaryActiveGameObject;
		float timer;

		public DoUpdater (TemporaryActiveGameObject temporaryActiveGameObject)
		{
			this.temporaryActiveGameObject = temporaryActiveGameObject;
			temporaryActiveGameObject.obj.SetActive(true);
		}
		
		public virtual void DoUpdate ()
		{
			if (temporaryActiveGameObject.realtime)
				timer += Time.unscaledDeltaTime;
			else
				timer += Time.deltaTime;
			if (timer >= temporaryActiveGameObject.duration)
			{
				if (temporaryActiveGameObject.obj != null)
					temporaryActiveGameObject.obj.SetActive(false);
				GameManager.updatables = GameManager.updatables.Remove(this);
			}
		}
	}
}