/**
 * main.js - 游戏入口
 * 启动时先加载所有精灵图，完成后再初始化游戏。
 */
// 全局错误捕获（不再破坏 DOM）
window.onerror = function(msg, src, line, col, err) {
    console.error('🚨 GLOBAL ERROR:', msg, '\nFile:', src + ':' + line, '\nStack:', err?.stack);
    // 不再覆盖 body.innerHTML，避免破坏 DOM
    return false;
};

// Dynamically resize canvas to match container (mobile full-screen fix)
function resizeCanvas() {
    const canvas = document.getElementById('game-canvas');
    const container = document.getElementById('game-canvas-container');
    if (!canvas || !container) return;
    const w = container.clientWidth;
    const h = container.clientHeight;
    if (w === 0 || h === 0) return;
    if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
        console.log('Canvas resized to', w, 'x', h);
    }
}
window.addEventListener('resize', resizeCanvas);

window.addEventListener('resize', resizeCanvas);

document.addEventListener('DOMContentLoaded', async () => {
    console.log('📦 DOMContentLoaded fired!');
    console.log('body exists:', !!document.body);
    console.log('game-canvas exists:', !!document.getElementById('game-canvas'));
    console.log('main-menu exists:', !!document.getElementById('main-menu'));

    resizeCanvas(); // set initial canvas size
    const canvas = document.getElementById('game-canvas');
    const statusEl = document.getElementById('loading-status') || createLoadingStatus();

    try {
        statusEl.textContent = '正在加载精灵图...';
        await window.spriteLoader.loadAll();
        statusEl.textContent = '加载完成！';
        console.log('✅ 所有精灵图加载完成');
    } catch (e) {
        console.warn('⚠️ 部分精灵图加载失败，将使用色块代替', e);
    }

    // 初始化游戏
    const game = new GameEngine(canvas);
    console.log('🎮 游戏已初始化', game);

    // 隐藏加载提示（只移除 loading-status 本身，不删父节点）
    console.log('statusEl:', statusEl.id, 'parentNode:', statusEl.parentNode?.id || statusEl.parentNode?.tagName);
    if (statusEl && statusEl.parentNode) {
        statusEl.remove();
        console.log('✅ loading-status 已移除');
    }

    game.renderMenuBackground();
    console.log('🖼️ 菜单背景已渲染');

    // DEBUG: 检查菜单可见性
    const menu = document.getElementById('main-menu');
    const container = document.getElementById('game-canvas-container');
    const canvasEl = document.getElementById('game-canvas');
    console.log('=== DEBUG ===');
    console.log('menu:', !!menu, 'container:', !!container, 'canvas:', !!canvasEl);
    console.log('body children:', document.body?.children?.length ?? 'NULL');
});

function createLoadingStatus() {
    const el = document.createElement('div');
    el.id = 'loading-status';
    el.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);'
                      + 'background:#000;color:#FFD700;padding:20px 32px;'
                      + 'border-radius:12px;font-size:18px;z-index:9999;';
    document.body.appendChild(el);
    return el;
}
