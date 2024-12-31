using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace Extensions
{
	public static class MathfExtensions
	{
		public const float INCHES_TO_CENTIMETERS = 2.54f;
		
		public static float SnapToInterval (float f, float interval)
		{
			if (interval == 0)
				return f;
			else
				return Mathf.Round(f / interval) * interval;
		}
		
		public static int Sign (float f)
		{
			if (f == 0)
				return 0;
			else
				return (int) Mathf.Sign(f);
		}
		
		public static bool AreOppositeSigns (float f1, float f2)
		{
			return Mathf.Abs(Sign(f1) - Sign(f2)) == 2;
		}

		public static float GetClosestNumber (float f, params float[] numbers)
		{
			float closestNumber = numbers[0];
			float closestDistance = Mathf.Abs(f - closestNumber);
			for (int i = 1; i < numbers.Length; i ++)
			{
				float number = numbers[i];
				float distance = Mathf.Abs(f - number);
				if (distance < closestDistance)
				{
					closestDistance = distance;
					closestNumber = number;
				}
			}
			return closestNumber;
		}

		public static int GetIndexOfClosestNumber (float f, params float[] numbers)
		{
			int output = 0;
			float closestNumber = numbers[0];
			float closestDistance = Mathf.Abs(f - closestNumber);
			for (int i = 1; i < numbers.Length; i ++)
			{
				float number = numbers[i];
				float distance = Mathf.Abs(f - number);
				if (distance < closestDistance)
				{
					closestDistance = distance;
					closestNumber = number;
					output = i;
				}
			}
			return output;
		}

		public static (float, int) GetClosestNumberAndIndex (float f, params float[] numbers)
		{
			int indexOfClosestNumer = 0;
			float closestNumber = numbers[0];
			float closestDistance = Mathf.Abs(f - closestNumber);
			for (int i = 1; i < numbers.Length; i ++)
			{
				float number = numbers[i];
				float distance = Mathf.Abs(f - number);
				if (distance < closestDistance)
				{
					closestDistance = distance;
					closestNumber = number;
					indexOfClosestNumer = i;
				}
			}
			return (closestNumber, indexOfClosestNumer);
		}

		public static float RegularizeAngle (float angle)
		{
			while (angle >= 360 || angle < 0)
				angle += Mathf.Sign(360 - angle) * 360;
			return angle;
		}

		public static float ClampAngle (float ang, float min, float max)
		{
			ang = RegularizeAngle(ang);
			min = RegularizeAngle(min);
			max = RegularizeAngle(max);
			float minDist = Mathf.Min(Mathf.DeltaAngle(ang, min), Mathf.DeltaAngle(ang, max));
			float _ang = WrapAngle(ang + Mathf.DeltaAngle(ang, minDist));
			if (_ang == min)
				return min;
			else if (_ang == max)
				return max;
			else
				return ang;
		}

		public static float WrapAngle (float ang)
		{
			if (ang < 0)
				ang += 360;
			else if (ang > 360)
				ang = 360 - ang;
			return ang;
		}

		public static float Round (float f, RoundingMethod roundingMethod)
		{
			if (roundingMethod == RoundingMethod.HalfOrMoreRoundsUp)
			{
				if (f % 1 >= 0.5f)
					return Mathf.Ceil(f);
			}
			else if (roundingMethod == RoundingMethod.HalfOrLessRoundsDown)
			{
				if (f % 1 <= 0.5f)
					return Mathf.Floor(f);
			}
			else if (roundingMethod == RoundingMethod.HalfOrMoreRoundsDown)
			{
				if (f % 1 >= 0.5f)
					return Mathf.Floor(f);
			}
			else if (roundingMethod == RoundingMethod.HalfOrLessRoundsUp)
			{
				if (f % 1 <= 0.5f)
					return Mathf.Ceil(f);
			}
			else if (roundingMethod == RoundingMethod.RoundUpIfNotInteger)
			{
				if (f % 1 != 0)
					return Mathf.Ceil(f);
			}
			else if (roundingMethod == RoundingMethod.RoundDownIfNotInteger)
			{
				if (f % 1 != 0)
					return Mathf.Floor(f);
			}
			else// if (roundingMethod == RoundingMethod.HalfOrLessRoundsDownElseRoundUp)
				return Mathf.Round(f);
			return f;
		}

		public static int RoundToInt (float f, RoundingMethod roundingMethod)
		{
			return (int) Round(f, roundingMethod);
		}

		public static float Lerp (float from, float to, float t)
		{
			return (1f - t) * from + to * t;
		}

		public static float InverseLerp (float from, float to, float value)
		{
			return (value - from) / (to - from);
		}

		public static float Remap (float inFrom, float inTo, float outFrom, float outTo, float value)
		{
			float t = InverseLerp(inFrom, inTo, value);
			return Lerp(outFrom, outTo, t);
		}

		public static float GetAverage (params float[] values)
		{
			float output = 0;
			for (int i = 0; i < values.Length; i ++)
			{
				float value = values[i];
				output += value;
			}
			return output / values.Length;
		}
		
		public enum RoundingMethod
		{
			HalfOrMoreRoundsUp,
			HalfOrLessRoundsDown,
			HalfOrMoreRoundsDown,
			HalfOrLessRoundsUp,
			RoundUpIfNotInteger,
			RoundDownIfNotInteger,
			HalfOrLessRoundsDownElseRoundUp
		}
	}
}