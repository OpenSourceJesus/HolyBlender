#if UNITY_EDITOR
using Extensions;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace HolyBlender
{
	public class RandomizePosition2D : EditorScript
	{
		public Transform trs;
		public Mode mode;
		public Collider2D collider;

		public override void Do ()
		{
			if (trs == null)
				trs = transform;
			if (mode == Mode.Circle)
				trs.position = collider.bounds.center + (Vector3) Random.insideUnitCircle.normalized * Random.value * collider.bounds.extents.x;
			else
				trs.position = collider.bounds.ToRect().RandomPoint();
		}

		public enum Mode
		{
			Circle,
			Box
		}
	}
}
#else
namespace HolyBlender
{
	public class RandomizePosition2D : EditorScript
	{
	}
}
#endif