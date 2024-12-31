using System;
using UnityEngine;
using Extensions;
using System.Collections.Generic;
// using System.Drawing;
// using System.Drawing.Drawing2D;

[Serializable]
public class Circle2D
{
	public Vector2 center;
	public float radius;
	public float Diameter
	{
		get
		{
			return radius * 2;
		}
		set
		{
			radius = value / 2;
		}
	}
	public float Circumference
	{
		get
		{
			return Mathf.PI * radius * 2;
		}
		set
		{
			radius = value / (Mathf.PI * 2);
		}
	}
	public float Area
	{
		get
		{
			return Mathf.PI * radius * radius;
		}
		set
		{
			radius = (float) Math.Sqrt(value / Math.PI);
		}
	}

	public Circle2D ()
	{
	}

	public Circle2D (float radius)
	{
		this.radius = radius;
	}

	public Circle2D (Vector2 center, float radius) : this (radius)
	{
		this.center = center;
	}

	public Vector2[] GetPointsAlongOutside (float addToAngle, float startAngle = 0)
	{
		Vector2[] output = new Vector2[0];
		float currentAngle = startAngle;
		do
		{
			output = output.Add(GetPointAtAngle(currentAngle));
			currentAngle += addToAngle;
		} while (Mathf.Abs(currentAngle - startAngle) <= 360f - Mathf.Abs(addToAngle));
		return output;
	}

	public Vector2 GetPointAtAngle (float angle)
	{
		return center + VectorExtensions.FromFacingAngle(angle) * radius;
	}

	public bool DoIIntersectWithLineSegment2D (LineSegment2D lineSegment)
	{
		Vector2 lineDirection = lineSegment.GetDirection();
		Vector2 centerToLineStart = lineSegment.start - center;
		float a = Vector2.Dot(lineDirection, lineDirection);
		float b = 2 * Vector2.Dot(centerToLineStart, lineDirection);
		float c = Vector2.Dot(centerToLineStart, centerToLineStart) - radius * radius;
		float discriminant = b * b - 4 * a * c;
		if (discriminant >= 0)
		{
			discriminant = Mathf.Sqrt(discriminant);
			float t1 = (-b - discriminant) / (2 * a);
			float t2 = (-b + discriminant) / (2 * a);
			if (t1 >= 0 && t1 <= 1 || t2 >= 0 && t2 <= 1)
				return true;
		}
		return false;
	}
	
	// public static Region GetIntersections (params Circle2D[] circles)
	// {
	// 	if (circles.Length == 0)
	// 		return null;
	// 	Region output = new Region();
	// 	for (int i = 0; i < circles.Length; i ++)
	// 	{
	// 		Circle2D circle = circles[i];
	// 		GraphicsPath circlePath = new GraphicsPath();
	// 		circlePath.AddEllipse(circle.center.x - circle.radius, circle.center.y - circle.radius, circle.radius * 2, circle.radius * 2);
	// 		output.Intersect(circlePath);
	// 	}
	// 	return output;
	// }

	// public static float GetIntersectionsArea (params Circle2D[] circles)
	// {
	// 	float output = 0;
	// 	RectangleF[] rectangles = GetIntersections(circles).GetRegionScans(new Matrix());
	// 	for (int i = 0; i < rectangles.Length; i ++)
	// 	{
	// 		RectangleF rectangle = rectangles[i];
	// 		output += rectangle.Width * rectangle.Height;
	// 	}
	// 	return output;
	// }

	// public Region ToRegion ()
	// {
	// 	GraphicsPath graphicsPath = new GraphicsPath();
	// 	graphicsPath.AddEllipse(center.x - radius, center.y - radius, radius * 2, radius * 2);
	// 	graphicsPath.Dispose();
	// 	Region region = new Region(graphicsPath);
	// 	region.Dispose();
	// 	return region;
	// }
}