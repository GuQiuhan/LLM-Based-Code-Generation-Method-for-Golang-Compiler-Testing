package main

import (
	"runtime"

	gogl "github.com/go-gl/gl"
	glfw "github.com/go-gl/glfw3"

	"github.com/dertseha/golgo/runner"
)



func setupGlfw() {
	glfw.WindowHint(glfw.ContextVersionMajor, 2)
	glfw.WindowHint(glfw.ContextVersionMinor, 0)
	glfw.SwapInterval(1)
}

func setupWindow(window *glfw.Window, application runner.Application) {
	window.SetSizeCallback(func(_ *glfw.Window, width int, height int) {
		application.Resize(width, height)
	})

	window.SetKeyCallback(getKeyCallback(application))

	window.MakeContextCurrent()
}

func getKeyCallback(application runner.Application) func(*glfw.Window, glfw.Key, int, glfw.Action, glfw.ModifierKey) {
	return func(window *glfw.Window, key glfw.Key, scancode int, action glfw.Action, modifier glfw.ModifierKey) {
		switch key {
		case glfw.KeyEscape:
			window.SetShouldClose(true)
		}
	}
}

func Run(application runner.Application, param runner.ApplicationParameter){
	runtime.LockOSThread()
	defer runtime.UnlockOSThread()

	if !glfw.Init() {
		panic("Failed to initialize GLFW")
	}
	defer glfw.Terminate()
	setupGlfw()

	window, err := glfw.CreateWindow(param.Width(), param.Height(), param.Title(), nil, nil)
	if err != nil {
		panic(err)
	}
	defer window.Destroy()
	setupWindow(window, application)

	gogl.Init()
	gl := CreateGles2Wrapper()

	application.Init(gl, param.Width(), param.Height())
	for !window.ShouldClose() {
		application.Render()

		window.SwapBuffers()
		glfw.PollEvents()
	}
}