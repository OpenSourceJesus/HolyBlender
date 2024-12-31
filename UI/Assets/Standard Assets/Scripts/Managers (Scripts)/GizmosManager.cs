using System;
using UnityEngine;
using System.Collections.Generic;

[ExecuteInEditMode]
public class GizmosManager : MonoBehaviour
{
	public static List<GizmosEntry> gizmosEntries = new List<GizmosEntry>();

	void OnDrawGizmos ()
	{
		for (int i = 0; i < gizmosEntries.Count; i ++)
		{
			GizmosEntry gizmosEntry = gizmosEntries[i];
			if (gizmosEntry.setColor)
				Gizmos.color = gizmosEntry.color;
			gizmosEntry.onDrawGizmos (gizmosEntry.arg);
			if (gizmosEntry.remove)
				gizmosEntries.RemoveAt(i);
		}
	}

	void OnDestroy ()
	{
		gizmosEntries.Clear();
	}

	public struct GizmosEntry
	{
		public Action<object> onDrawGizmos;
		public object arg;
		public bool setColor;
		public Color color;
		public bool remove;
	}
}