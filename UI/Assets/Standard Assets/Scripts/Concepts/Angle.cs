using System;
using Extensions;
using UnityEngine;

[Serializable]
public class Angle
{
	public float degrees;
	public float NormalizedDegrees
	{
		get
		{
			return degrees / 360;
		}
		set
		{
			degrees = value * 360;
		}
	}
	public float Radians
	{
		get
		{
			return degrees * Mathf.Deg2Rad;
		}
		set
		{
			degrees = value * Mathf.Rad2Deg;
		}
	}

	public Angle ()
	{
	}

	public Angle (float degrees)
	{
		this.degrees = degrees;
	}

	public virtual bool IsWithinAngleRange (AngleRange angleRange, bool equalAnglesIntersect = true)
	{
		return angleRange.Contains(this, equalAnglesIntersect);
	}

	public virtual Angle Unwrapped ()
	{
		return Wrap(-GetWrappedAmount());
	}

	public virtual Angle Wrap (float wraps, bool clockwise = false)
	{
		if (clockwise)
			return new Angle(degrees - wraps * 360);
		else
			return new Angle(degrees + wraps * 360);
	}

	public virtual float GetWrappedAmount ()
	{
		return degrees % 360;
	}
}