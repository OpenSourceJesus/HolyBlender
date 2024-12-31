using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace Extensions
{
	public static class QuaternionExtensions
	{
		public static Quaternion INFINITE = new Quaternion(Mathf.Infinity, Mathf.Infinity, Mathf.Infinity, Mathf.Infinity);

		public static Vector3 GetDeltaAngles (Vector3 fromEulerAngles, Vector3 toEulerAngles)
		{
			return new Vector3(Mathf.DeltaAngle(fromEulerAngles.x, toEulerAngles.x), Mathf.DeltaAngle(fromEulerAngles.y, toEulerAngles.y), Mathf.DeltaAngle(fromEulerAngles.z, toEulerAngles.z));
		}

		public static Vector3 GetDeltaAngles (Quaternion fromRotation, Quaternion toRotation)
		{
			Vector3 fromEulerAngles = fromRotation.eulerAngles;
			Vector3 toEulerAngles = toRotation.eulerAngles;
			return GetDeltaAngles(fromEulerAngles, toEulerAngles);
		}

		public static Vector3 GetAngularVelocity (Quaternion fromRotation, Quaternion toRotation)
		{
			return GetDeltaAngles(fromRotation, toRotation) / Time.deltaTime;
		}

		public static Vector3 GetAngularVelocity (Vector3 fromEulerAngles, Vector3 toEulerAngles)
		{
			return GetDeltaAngles(fromEulerAngles, toEulerAngles) / Time.deltaTime;
		}

		public static Quaternion[] GetRotationsForTurn (Quaternion startRotation, Quaternion endRotation, int stepCount)
		{
			Quaternion[] rotations = new Quaternion[stepCount];
			float angle = Quaternion.Angle(startRotation, endRotation);
			for (int i = 0; i < stepCount; i ++)
			{
				Quaternion rotation = Quaternion.RotateTowards(startRotation, endRotation, angle / stepCount * (i + 1));
				rotations[i] = rotation;
			}
			return rotations;
		}
	}
}