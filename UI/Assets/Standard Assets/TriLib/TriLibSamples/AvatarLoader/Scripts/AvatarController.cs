using UnityEngine;

namespace TriLibCore.Samples
{
    /// <summary>Represents a class used to control an avatar on TriLib samples.</summary>
    public class AvatarController : AbstractInputSystem
    {
        /// <summary>The Avatar Controller Singleton instance.</summary>
        public static AvatarController Instance { get; private set; }

        /// <summary>
        /// Maximum avatar speed in units/second.
        /// </summary>
        private const float MaxSpeed = 2f;

        /// <summary>
        /// Avatar acceleration in units/second.
        /// </summary>
        private const float Acceleration = 5f;

        /// <summary>
        /// Avatar Friction in units/second.
        /// </summary>
        private const float Friction = 2f;

        /// <summary>
        /// Avatar smooth rotation factor.
        /// </summary>
        private const float RotationSpeed = 60f;

        /// <summary>
        /// Avatar character controller.
        /// </summary>
        public CharacterController CharacterController;

        /// <summary>
        /// Avatar animator.
        /// </summary>
        public Animator Animator;

        /// <summary>
        /// Game object that wraps the actual avatar.
        /// </summary>
        public GameObject InnerAvatar;

        /// <summary>
        /// Camera offset relative to the avatar.
        /// </summary>
        private Vector3 _cameraOffset;

        /// <summary>
        /// Current avatar speed.
        /// </summary>
        private float _speed;

        /// <summary>
        /// Camera height offset relative to the avatar.
        /// </summary>
        private Vector3 _cameraHeightOffset;


        /// <summary>
        /// Current smooth rotation velocity.
        /// </summary>
        private float _currentVelocity;

        /// <summary>Configures this instance and calculates the Camera offsets.</summary>
        private void Awake()
        {
            Instance = this;
            _cameraHeightOffset = new Vector3(0f, CharacterController.height * 0.8f, 0f);
            _cameraOffset = Camera.main.transform.position - transform.position;
        }

        /// <summary>Handles input (controls the Camera and moves the Avatar character).</summary>
        private void Update()
        {
            var input = new Vector3(GetAxis("Horizontal"), 0f, GetAxis("Vertical"));
            var direction = Camera.main.transform.TransformDirection(input);
            direction.y = 0f;
            direction.Normalize();
            var targetEulerAngles = direction.magnitude > 0 ? Quaternion.LookRotation(direction).eulerAngles : transform.rotation.eulerAngles;
            var eulerAngles = transform.rotation.eulerAngles;
            eulerAngles.y = Mathf.SmoothDampAngle(eulerAngles.y, targetEulerAngles.y, ref _currentVelocity, Time.deltaTime * RotationSpeed * input.magnitude);
            transform.rotation = Quaternion.Euler(eulerAngles);
            _speed += input.magnitude * (Acceleration * MaxSpeed) * Time.deltaTime;
            _speed -= Friction * MaxSpeed * Time.deltaTime;
            _speed = Mathf.Clamp(_speed, 0f, MaxSpeed);
            CharacterController.SimpleMove(transform.forward * _speed);
            Animator.SetFloat("SpeedFactor", _speed / MaxSpeed);
            var pivotedPosition = Quaternion.AngleAxis(AssetViewerBase.Instance.CameraAngle.x, Vector3.up) * Quaternion.AngleAxis(-AssetViewerBase.Instance.CameraAngle.y, Vector3.right) * _cameraOffset;
            Camera.main.transform.position = transform.position + _cameraHeightOffset + pivotedPosition;
            Camera.main.transform.LookAt(transform.position + _cameraHeightOffset);
        }
    }
}
