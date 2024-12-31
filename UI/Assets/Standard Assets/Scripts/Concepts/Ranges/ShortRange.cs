/*
	This file defines a Range of shorts
*/

using System;
using Extensions;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

[Serializable]
public class ShortRange : Range<short>
{
	public ShortRange ()
	{
	}

	public ShortRange (short min, short max) : base (min, max)
	{
	}

	public bool DoesIntersect (ShortRange shortRange, bool equalIntsIntersect = true)
	{
		if (equalIntsIntersect)
			return (min >= shortRange.min && min <= shortRange.max) || (shortRange.min >= min && shortRange.min <= max) || (max <= shortRange.max && max >= shortRange.min) || (shortRange.max <= max && shortRange.max >= min);
		else
			return (min > shortRange.min && min < shortRange.max) || (shortRange.min > min && shortRange.min < max) || (max < shortRange.max && max > shortRange.min) || (shortRange.max < max && shortRange.max > min);
	}

	public bool GetIntersectionRange (ShortRange shortRange, out ShortRange? intersectionRange, bool equalIntsIntersect = true)
	{
		intersectionRange = null;
		if (DoesIntersect(shortRange, equalIntsIntersect))
			intersectionRange = new ShortRange((short) Mathf.Max(min, shortRange.min), (short) Mathf.Min(max, shortRange.max));
		return intersectionRange != null;
	}

	public override short Get (float normalizedValue)
	{
		return (short) Mathf.RoundToInt((max - min) * normalizedValue + min);
	}

	public override bool Contains (short value, bool includeMinAndMax = true)
	{
		if (includeMinAndMax)
			return value >= min && value <= max;
		else
			return value > min && value < max;
	}
}