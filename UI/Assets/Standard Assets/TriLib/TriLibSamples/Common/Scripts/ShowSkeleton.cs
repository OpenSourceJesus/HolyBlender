using System;
using System.Collections.Generic;
using TriLibCore.Extensions;
using UnityEngine;

namespace TriLibCore.Samples
{
    public class ShowSkeleton : MonoBehaviour
    {
        private List<Transform> _bones;

        private static Material _material;

        public void Setup(AssetLoaderContext assetLoaderContext, AssetViewer assetViewer)
        {
            _bones = new List<Transform>();
            assetLoaderContext.RootModel.GetBones(assetLoaderContext, _bones);
            if (_bones.Count > 0)
            {
                SetCustomBounds(assetViewer);
            }
        }

        private void Start()
        {
            if (_material == null)
            {
                _material = new Material(Shader.Find("Hidden/ShowSkeleton"));
            }
            if (_bones == null)
            {
                _bones = new List<Transform>();
                var transforms = GetComponentsInChildren<Transform>();
                foreach (var transform in transforms)
                {
                    _bones.Add(transform);
                }
            }
        }

        private void SetCustomBounds(AssetViewer assetViewer)
        {
            var totalBounds = new Bounds();
            var totalBoundsInitialized = false;
            if (assetViewer.RootGameObject.TryGetComponent<Animation>(out var animation))
            {
                var animationClips = animation.GetAllAnimationClips();
                foreach (var clip in animationClips)
                {
                    animation.clip = clip;
                    var frameInterval = 1f / clip.frameRate;
                    for (var t = 0f; t < clip.length; t += frameInterval)
                    {
                        animation[clip.name].time = t;
                        animation.Sample();
                        var bounds = new Bounds();
                        var initialized = false;
                        foreach (var bone in _bones)
                        {
                            if (!initialized)
                            {
                                bounds.center = bone.position;
                                if (!totalBoundsInitialized)
                                {
                                    totalBounds.center = bone.position;
                                    totalBoundsInitialized = true;
                                }
                                initialized = true;
                            }
                            else
                            {
                                bounds.Encapsulate(bone.position);
                            }
                        }
                        totalBounds.Encapsulate(bounds);
                    }
                }
            }
            if (totalBounds.size.magnitude > 0f)
            {
                assetViewer.SetCustomBounds(totalBounds);
            }
        }

        private void OnDrawGizmos()
        {
            if (_bones != null)
            {
                foreach (var transform in _bones)
                {
                    foreach (Transform child in transform)
                    {
                        Gizmos.color = Color.green;
                        Gizmos.DrawLine(transform.position, child.position);
                    }
                }
            }
        }

        private void OnRenderObject()
        {
            _material.SetPass(0);
            GL.PushMatrix();
            GL.Begin(GL.LINES);
            foreach (var transform in _bones)
            {
                foreach (Transform child in transform)
                {
                    GL.Color(Color.green);
                    GL.Vertex(transform.position);
                    GL.Vertex(child.position);
                }
            }
            GL.End();
            GL.PopMatrix();
        }
    }
}