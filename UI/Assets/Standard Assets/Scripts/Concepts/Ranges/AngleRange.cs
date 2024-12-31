using System;
using Extensions;
using UnityEngine;

[Serializable]
public class AngleRange : Range<Angle>
{
	public float Degrees
	{
		get
		{
			return max.degrees - min.degrees;
		}
		set
		{
			Angle previousMin = min;
			min = new Angle(max.degrees - value);
			max = new Angle(previousMin.degrees + value);
		}
	}

	public AngleRange ()
	{
	}

	public AngleRange (Angle min, Angle max) : base (min, max)
	{
	}

	public bool DoesIntersect (AngleRange angleRange, bool equalAnglesIntersect = true)
	{
		if (equalAnglesIntersect)
			return (min.degrees >= angleRange.min.degrees && min.degrees <= angleRange.max.degrees) || (angleRange.min.degrees >= min.degrees && angleRange.min.degrees <= max.degrees) || (max.degrees <= angleRange.max.degrees && max.degrees >= angleRange.min.degrees) || (angleRange.max.degrees <= max.degrees && angleRange.max.degrees >= min.degrees);
		else
			return (min.degrees > angleRange.min.degrees && min.degrees < angleRange.max.degrees) || (angleRange.min.degrees > min.degrees && angleRange.min.degrees < max.degrees) || (max.degrees < angleRange.max.degrees && max.degrees > angleRange.min.degrees) || (angleRange.max.degrees < max.degrees && angleRange.max.degrees > min.degrees);
	}

	public bool Contains (Angle angle, bool equalAnglesIntersect = true)
	{
		if (equalAnglesIntersect)
			return Mathf.Abs(Vector2.Angle(VectorExtensions.FromFacingAngle(angle.degrees), VectorExtensions.FromFacingAngle(min.degrees)) - Vector2.Angle(VectorExtensions.FromFacingAngle(angle.degrees), VectorExtensions.FromFacingAngle(max.degrees))) <= Degrees;
		else
			return Mathf.Abs(Vector2.Angle(VectorExtensions.FromFacingAngle(angle.degrees), VectorExtensions.FromFacingAngle(min.degrees)) - Vector2.Angle(VectorExtensions.FromFacingAngle(angle.degrees), VectorExtensions.FromFacingAngle(max.degrees))) < Degrees;
	}

	// public bool GetIntersectionRange (AngleRange angleRange, out AngleRange intersectionRange, bool equalAnglesIntersect = true)
	// {
	// 	intersectionRange = NULL;
	// 	if (DoesIntersect(angleRange, equalAnglesIntersect))
	// 	{
	// 		intersectionRange = new AngleRange(Mathf.Max.degrees(min.degrees, angleRange.min.degrees), Mathf.Min.degrees(max.degrees, angleRange.max.degrees));
	// 	}
	// 	return intersectionRange != NULL;
	// }
}