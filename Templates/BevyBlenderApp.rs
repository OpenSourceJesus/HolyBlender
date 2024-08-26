use std::ops::Mul;
use bevy::prelude::*;
use bevy::window::WindowRef;
use bevy_rapier3d::prelude::*;
use bevy::window::PrimaryWindow;
use bevy_asset_loader::prelude::*;
use bevy::render::camera::RenderTarget;
use bevy_gltf_components::ComponentsFromGltfPlugin;

fn main() {
	let app = App::new()
		ꗈ0
		.add_plugins((
			DefaultPlugins,
			ComponentsFromGltfPlugin::default()
		))
		.init_state::<MyStates>()
		.add_loading_state(
			LoadingState::new(MyStates::AssetLoading)
				.continue_to_state(MyStates::Next)
				.load_collection::<LevelAssets>(),
		)
		.add_systems(OnEnter(MyStates::Next), StartLevel)
		.add_systems(Update, SetCursorPoint)
		.add_event::<ScreenToWorldPointEvent>()
		.add_systems(Update, ScreenToWorldPoint)
		ꗈ1
		.run();
}

#[derive(AssetCollection, Resource)]
struct LevelAssets {
	#[asset(path = "ꗈ2#Scene0")]
	level: Handle<Scene>,
}

fn StartLevel (
	mut commands: Commands,
	assets: Res<LevelAssets>,
	assetServer: Res<AssetServer>,
	mut meshes : ResMut<Assets<Mesh>>,
	keys: Res<ButtonInput<KeyCode>>,
	mouseButtons: Res<ButtonInput<MouseButton>>,
	mut cursorEvent: EventReader<CursorMoved>,
	mut screenToWorldPointEvent: EventWriter<ScreenToWorldPointEvent>
) {
	unsafe
	{
		ꗈ3
		commands.spawn((
			SceneBundle {
				scene: assets.level.clone(),
				..default()
			},
			Name::new("Game"),
		));
	}
}

#[derive(
	Clone, Eq, PartialEq, Debug, Hash, Default, States,
)]
enum MyStates {
	#[default]
	AssetLoading,
	Next,
}

#[derive(Event)]
struct RemoveComponentEvent(&'static str);

fn SpawnEntity (commands: &mut Commands, assetServer: &Res<AssetServer>, assetPath : &'static str, position : Vec3, rotation : Quat) -> Entity
{
	return commands.spawn((SceneBundle {
		transform: Transform::from_translation(position).with_rotation(rotation),
		scene: assetServer.load(assetPath),
			..default()
		},
	)).id();
}

static mut cursorPoint : Vec3 = Vec3::ZERO;

fn SetCursorPoint (
    q_window_primary : Query<&Window, With<PrimaryWindow>>,
    q_window : Query<&Window>,
    mut q_camera : Query<(&Camera, &GlobalTransform)>,
) {
    for (camera, camera_transform) in &mut q_camera {
        let window = match camera.target {
			RenderTarget::Window(WindowRef::Primary) => {
                q_window_primary.single()
            },
            RenderTarget::Window(WindowRef::Entity(e_window)) => {
                q_window.get(e_window).unwrap()
            },
            _ => {
                continue;
            }
        };
		if let Some(world_position) = window.cursor_position()
        {
			unsafe
			{
				cursorPoint = Vec3::new(world_position.x, world_position.y, 0.0);
			}
        }
    }
}

fn GetScreenToWorldPoint (screenPoint : Vec3, mut screenToWorldPointEvent: &mut EventWriter<ScreenToWorldPointEvent>) -> Vec3
{
	screenToWorldPointEvent.send(ScreenToWorldPointEvent(screenPoint));
	unsafe
	{
		return worldPoint;
	}
}

#[derive(Event)]
struct ScreenToWorldPointEvent(Vec3);

static mut worldPoint : Vec3 = Vec3::ZERO;

fn ScreenToWorldPoint (
    q_window_primary : Query<&Window, With<PrimaryWindow>>,
    q_window : Query<&Window>,
    mut q_camera : Query<(&Camera, &GlobalTransform)>,
    mut screenToWorldPointEvent: EventReader<ScreenToWorldPointEvent>
)
{
    for (camera, camera_transform) in &mut q_camera {
        let window = match camera.target {
			RenderTarget::Window(WindowRef::Primary) => {
                q_window_primary.single()
            },
            RenderTarget::Window(WindowRef::Entity(e_window)) => {
                q_window.get(e_window).unwrap()
            },
            _ => {
                continue;
            }
        };
		let mut screenPoint : Vec3 = Vec3::ZERO;
		for event in screenToWorldPointEvent.read()
		{
			screenPoint = event.0;
		}
		let ray = camera.viewport_to_world(camera_transform, Vec2::new(screenPoint.x, screenPoint.y));
		if ray != None
		{
			unsafe
			{
				worldPoint = ray.unwrap().origin;
			}
		}
    }
}