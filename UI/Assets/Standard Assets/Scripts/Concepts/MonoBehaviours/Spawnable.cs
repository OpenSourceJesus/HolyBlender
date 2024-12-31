using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace HolyBlender
{
	[ExecuteInEditMode]
	public class Spawnable : MonoBehaviour, ISpawnable
	{
		public Transform trs;
		public int prefabIndex;
		public int PrefabIndex
		{
			get
			{
				return prefabIndex;
			}
		}

		public virtual void Start ()
		{
#if UNITY_EDITOR
			if (!Application.isPlaying)
			{
				if (trs == null)
					trs = GetComponent<Transform>();
				return;
			}
#endif
		}
	}
}