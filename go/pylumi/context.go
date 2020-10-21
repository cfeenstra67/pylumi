package pylumi

import (
    "fmt"
    // "path/filepath"

    "github.com/blang/semver"

    // "github.com/pulumi/pulumi/pkg/v2/engine"
    "github.com/pulumi/pulumi/sdk/v2/go/common/diag"
    "github.com/pulumi/pulumi/sdk/v2/go/common/resource/plugin"
    "github.com/pulumi/pulumi/sdk/v2/go/common/tokens"
    "github.com/pulumi/pulumi/sdk/v2/go/common/workspace"
)

type Context struct {
    // Info engine.Projinfo
    PluginCtx *plugin.Context
    WorkingDirectory string
    // Main string
    Sink diag.Sink
    StatusSink diag.Sink
    providers map[tokens.Package]*plugin.Provider
}

func NewContextFromPath(cwd string, sink, statusSink diag.Sink) (*Context, error) {
    // projectPath, err := workspace.DetectProjectPathFrom(path)
    // if err != nil {
    //  return nil, fmt.Errorf("error detecting project: %v", err)
    // }

    // proj, err := workspace.LoadProject(path)
    // if err != nil {
    //  return nil, fmt.Errorf("error loading project: %v", err)
    // }

    // root := filepath.Dir(path)

    // projInfo := engine.Projinfo{Proj: proj, Root: root}

    // pwd, main, ctx, err := engine.ProjectInfoContext(&projInfo, nil, nil, sink, statusSink, false, nil)

    ctx, err := plugin.NewContext(sink, statusSink, nil, nil, cwd, nil, false, nil)
    if err != nil {
        return nil, fmt.Errorf("error obtaining context: %v", err)
    }

    newCtx := Context{
        // Info: projInfo,
        PluginCtx: ctx,
        WorkingDirectory: cwd,
        // Main: main,
        Sink: sink,
        StatusSink: statusSink,
    }

    return &newCtx, nil
}

func (c *Context) Close() {
    c.PluginCtx.Close()
}

// func (c *Context) InstallPlugins() error {
//  return engine.RunInstallPlugins(
//      c.Info.Proj, c.WorkingDirectory, c.Main, nil, c.PluginCtx,
//  )
// }

func (c *Context) Provider(name tokens.Package, version *semver.Version) (*plugin.Provider, error) {
    if c.providers == nil {
        c.providers = make(map[tokens.Package]*plugin.Provider)
    }

    provider, ok := c.providers[name]
    if !ok {
        providerValue, err := c.PluginCtx.Host.Provider(name, version)
        if err != nil {
            return nil, fmt.Errorf("error getting provider: %v", err)
        }
        c.providers[name] = &providerValue
        provider = &providerValue
    }
    return provider, nil
}

func (c *Context) CloseProvider(name tokens.Package) error {
    provider, ok := c.providers[name]
    if !ok {
        return nil
    }
    if err := c.PluginCtx.Host.CloseProvider(*provider); err != nil {
        return fmt.Errorf("error closing provider: %v", err)
    }
    delete(c.providers, name)
    return nil
}

func (c *Context) CloseProviders() error {
    for key, _ := range c.providers {
        if err := c.CloseProvider(key); err != nil {
            return err
        }
    }
    return nil
}

func (c *Context) ListPlugins() []workspace.PluginInfo {
    return c.PluginCtx.Host.ListPlugins()
}
