import type { Meta, StoryObj } from '@storybook/react';
import Badge from './Badge';

const meta  : Meta<typeof Badge> = {
  title: 'Components/Badge',
  component: Badge,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Badge>;

export const Dot: Story = { args={{ children: <span>Icon</span> }} };
export const WithCount: Story = { args={{ count: 5, children: <span>Icon</span> }} };
