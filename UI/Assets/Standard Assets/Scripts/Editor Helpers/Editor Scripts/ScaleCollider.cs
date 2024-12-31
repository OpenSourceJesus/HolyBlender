#if UNITY_EDITOR
using UnityEngine;
using Extensions;

namespace HolyBlender
{
	public class ScaleCollider : EditorScript
	{
		public Collider2D collider;
		public Vector3 scale;

		public override void Do ()
		{
			if (collider == null)
				collider = GetComponent<Collider2D>();
			PolygonCollider2D polygonCollider = collider as PolygonCollider2D;
			if (polygonCollider != null)
			{
				Vector2[] points = polygonCollider.points;
				for (int i = 0; i < points.Length ; i ++)
					points[i] *= scale;
				polygonCollider.points = points;
			}
		}
	}
}
#else
namespace HolyBlender
{
	public class ScaleCollider : EditorScript
	{
	}
}
#endif