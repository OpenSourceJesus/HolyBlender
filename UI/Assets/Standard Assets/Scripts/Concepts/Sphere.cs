using System;
using UnityEngine;

[Serializable]
public class Sphere
{
    public Vector3 center;
    public float radius;

    public Sphere (Vector3 center, float radius)
    {
        this.center = center;
        this.radius = radius;
    }
}