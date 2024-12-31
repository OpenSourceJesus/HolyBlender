using System;
using UnityEngine;

namespace TriLibCore.Mappers
{
    /// <summary>Represents a Mapper that converts legacy Animation Clips into humanoid Animation Clips.</summary>
    [CreateAssetMenu(menuName = "TriLib/Mappers/Animation Clip/Legacy To Humanoid Animation Clip Mapper", fileName = "LegacyToHumanoidAnimationClipMapper")]

	[Obsolete("This mapper is not used anymore as Unity does not support runtime Generic AnimationClips creation")]
    public class LegacyToHumanoidAnimationClipMapper : AnimationClipMapper
    {
        /// <summary>
        /// Template mecanim animation clip.
        /// Unity runtime API can't access mecanim animation clip settings as root motion baking, animation loop mode, etc.
        /// So we get these settings from the template animation clip.
        /// </summary>
        public AnimationClip MecanimAnimationClipTemplate;

        /// <inheritdoc/>
        public override AnimationClip[] MapArray(AssetLoaderContext assetLoaderContext, AnimationClip[] sourceAnimationClips)
        {
            return sourceAnimationClips;
        }
    }
}