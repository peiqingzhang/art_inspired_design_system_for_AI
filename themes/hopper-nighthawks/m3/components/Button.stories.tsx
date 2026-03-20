import type { Meta, StoryObj } from '@storybook/react';
import Button from './Button';

const meta  : Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Filled: Story = { args={{ variant: 'filled', children: 'Click me' }} };
export const Outlined: Story = { args={{ variant: 'outlined', children: 'Click me' }} };
export const Tonal: Story = { args={{ variant: 'tonal', children: 'Click me' }} };
export const Text: Story = { args={{ variant: 'text', children: 'Click me' }} };
