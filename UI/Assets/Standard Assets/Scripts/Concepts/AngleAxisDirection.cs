using System;
using Extensions;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

[Serializable]
public class AngleAxisDirection
{
	public float xyAngle;
	public float xzAngle;
	public float yzAngle;
	public Vector3 direction;

	public AngleAxisDirection (float xyAngle, float xzAngle, float yzAngle)
	{
		this.xyAngle = xyAngle;
		this.xzAngle = xzAngle;
		this.yzAngle = yzAngle;
	}
	
	public Vector3 GetValue ()
	{
		Vector3 output;
		Vector2 xyVector = new Vector2();
		Vector2 xzVector = new Vector2();
		Vector2 yzVector = new Vector2();
		if (xyAngle != 0)
			xyVector = VectorExtensions.FromFacingAngle(xyAngle);
		if (xzAngle != 0)
			xzVector = VectorExtensions.FromFacingAngle(xzAngle);
		if (yzAngle != 0)
			yzVector = VectorExtensions.FromFacingAngle(yzAngle);
		output = new Vector3(xyVector.x + xzVector.x, xyVector.y + yzVector.x, xzVector.y + yzVector.y).normalized;
		direction = output;
		return output;
	}
	
	public AngleAxisDirection Add (AngleAxisDirection angleAxisDirection)
	{
		xyAngle += angleAxisDirection.xyAngle;
		xzAngle += angleAxisDirection.xzAngle;
		yzAngle += angleAxisDirection.yzAngle;
		return this;
	}
	
	public AngleAxisDirection Multiply (AngleAxisDirection angleAxisDirection)
	{
		xyAngle *= angleAxisDirection.xyAngle;
		xzAngle *= angleAxisDirection.xzAngle;
		yzAngle *= angleAxisDirection.yzAngle;
		return this;
	}
}
