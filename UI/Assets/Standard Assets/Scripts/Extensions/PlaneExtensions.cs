using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Extensions
{
	public static class PlaneExtensions
	{
		public static bool Raycast (this Plane plane, Ray ray, out Vector3 hitPoint)
		{
			hitPoint = VectorExtensions.INFINITE3;
			float distance = 0;
			if (plane.Raycast(ray, out distance))
			{
				hitPoint = ray.GetPoint(distance);
				return true;
			}
			else
				return false;
		}
	}
}