using System;
using UnityEngine;
using UnityEngine.Rendering;

namespace Extensions
{
	public static class MaterialExtensions
	{
		public static void ChangeMaterialTransparency (this Material material, bool shouldMakeTransparent)
		{
			if (shouldMakeTransparent)
			{
				material.SetFloat("_Surface", (float) SurfaceType.Transparent);
				material.SetFloat("_Blend", (float) BlendMode.Alpha);
			}
			else
				material.SetFloat("_Surface", (float) SurfaceType.Opaque);
			SetupMaterialBlendMode (material);
		}

		public static void SetupMaterialBlendMode (this Material material)
		{
			if (material == null)
				throw new ArgumentNullException("material");
			bool alphaClip = material.GetFloat("_AlphaClip") == 1;
			if (alphaClip)
				material.EnableKeyword("_ALPHATEST_ON");
			else
				material.DisableKeyword("_ALPHATEST_ON");
			SurfaceType surfaceType = (SurfaceType) material.GetFloat("_Surface");
			if (surfaceType == 0)
			{
				material.SetOverrideTag("RenderType", "");
				material.SetInt("_SrcBlend", (int) UnityEngine.Rendering.BlendMode.One);
				material.SetInt("_DstBlend", (int) UnityEngine.Rendering.BlendMode.Zero);
				material.SetInt("_ZWrite", 1);
				material.DisableKeyword("_ALPHAPREMULTIPLY_ON");
				material.renderQueue = -1;
				material.SetShaderPassEnabled("ShadowCaster", true);
			}
			else
			{
				BlendMode blendMode = (BlendMode) material.GetFloat("_Blend");
				switch (blendMode)
				{
					case BlendMode.Alpha:
						material.SetOverrideTag("RenderType", "Transparent");
						material.SetInt("_SrcBlend", (int) UnityEngine.Rendering.BlendMode.SrcAlpha);
						material.SetInt("_DstBlend", (int) UnityEngine.Rendering.BlendMode.OneMinusSrcAlpha);
						material.SetInt("_ZWrite", 0);
						material.DisableKeyword("_ALPHAPREMULTIPLY_ON");
						material.renderQueue = (int) UnityEngine.Rendering.RenderQueue.Transparent;
						material.SetShaderPassEnabled("ShadowCaster", false);
						break;
					case BlendMode.Premultiply:
						material.SetOverrideTag("RenderType", "Transparent");
						material.SetInt("_SrcBlend", (int) UnityEngine.Rendering.BlendMode.One);
						material.SetInt("_DstBlend", (int) UnityEngine.Rendering.BlendMode.OneMinusSrcAlpha);
						material.SetInt("_ZWrite", 0);
						material.EnableKeyword("_ALPHAPREMULTIPLY_ON");
						material.renderQueue = (int) UnityEngine.Rendering.RenderQueue.Transparent;
						material.SetShaderPassEnabled("ShadowCaster", false);
						break;
					case BlendMode.Additive:
						material.SetOverrideTag("RenderType", "Transparent");
						material.SetInt("_SrcBlend", (int) UnityEngine.Rendering.BlendMode.One);
						material.SetInt("_DstBlend", (int) UnityEngine.Rendering.BlendMode.One);
						material.SetInt("_ZWrite", 0);
						material.DisableKeyword("_ALPHAPREMULTIPLY_ON");
						material.renderQueue = (int) UnityEngine.Rendering.RenderQueue.Transparent;
						material.SetShaderPassEnabled("ShadowCaster", false);
						break;
					case BlendMode.Multiply:
						material.SetOverrideTag("RenderType", "Transparent");
						material.SetInt("_SrcBlend", (int) UnityEngine.Rendering.BlendMode.DstColor);
						material.SetInt("_DstBlend", (int) UnityEngine.Rendering.BlendMode.Zero);
						material.SetInt("_ZWrite", 0);
						material.DisableKeyword("_ALPHAPREMULTIPLY_ON");
						material.renderQueue = (int) UnityEngine.Rendering.RenderQueue.Transparent;
						material.SetShaderPassEnabled("ShadowCaster", false);
						break;
				}
			}
		}

		enum SurfaceType
		{
			Opaque,
			Transparent
		}

		enum BlendMode
		{
			Alpha,
			Premultiply,
			Additive,
			Multiply
		}
	}
}